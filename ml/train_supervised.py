import mlflow
import mlflow.sklearn
from mlflow.tracking import MlflowClient
from sklearn.model_selection import train_test_split
from sklearn.ensemble import RandomForestClassifier
from sklearn.metrics import roc_auc_score, precision_score, recall_score
from sklearn.impute import SimpleImputer
from sklearn.compose import ColumnTransformer
from sklearn.pipeline import Pipeline
from sklearn.preprocessing import PowerTransformer
from sklearn.preprocessing import FunctionTransformer, OneHotEncoder
from sklearn.pipeline import Pipeline
from ml.utils import load_feature_data
from pandas.api.types import is_numeric_dtype
import numpy as np
from mlflow.models import infer_signature

MODEL_NAME = "WarrantyModel"


def train():

    mlflow.set_tracking_uri("file:./mlruns")
    mlflow.set_experiment("Warranty_Prediction")

    df = load_feature_data().dropna()

    X = df.drop(["vehicle_id", "warranty_flag", "feature_snapshot_timestamp" , "data_version"], axis=1)
    y = df["warranty_flag"]

    yj_cols = []
    log_cols = []

    for col in X.columns:
        # Only consider numeric columns for transformations that expect numbers
        if not is_numeric_dtype(X[col]):
            # leave non-numeric columns out of numeric pipelines; they will be
            # passed through by the ColumnTransformer remainder
            continue

        if (
            X[col].max() < 1e6 and
            X[col].skew() < 2 and
            X[col].nunique() > 10
        ):
            yj_cols.append(col)
        else:
            log_cols.append(col)

    def clip_function(x):
        return np.clip(x, -0.999, None)

    numeric_log_pipe = Pipeline([
            ("clip", FunctionTransformer(clip_function, validate=False)),
                ("log", FunctionTransformer(np.log1p, validate=False))
                ])

    numeric_yj_pipe = Pipeline([
        ( "power", PowerTransformer(method="yeo-johnson"))])



    X_train, X_test, y_train, y_test = train_test_split(
        X, y, test_size=0.2, random_state=42
    )

    
    with mlflow.start_run() as run:

        # Training hyperparameters
        n_estimators = 100
        random_state = 42
        max_samples = 0.5
        max_features = 0.75
        max_depth = 15
        class_weight = "balanced"

        # Build classifier
        clf = RandomForestClassifier(
            n_estimators=n_estimators,
            random_state=random_state,
            max_samples=max_samples,
            max_features=max_features,
            max_depth=max_depth,
            class_weight=class_weight,
        )

        # Preprocessor + classifier pipeline so we can fit/predict and log the
        # whole pipeline via MLflow.
        # Identify categorical (non-numeric) columns to encode
        cat_cols = [c for c in X.columns if not is_numeric_dtype(X[c])]

        transformers = [
            ("num_log", numeric_log_pipe, log_cols),
            ("num_yj", numeric_yj_pipe, yj_cols),
        ]

        if cat_cols:
            transformers.append(("cat", OneHotEncoder(handle_unknown="ignore"), cat_cols))

        preprocessor = ColumnTransformer(transformers=transformers, remainder="passthrough")

        full_pipeline = Pipeline([
            ("preprocessor", preprocessor),
            ("classifier", clf),
        ])

        # Fit and predict using the full pipeline
        full_pipeline.fit(X_train, y_train)
        y_pred = full_pipeline.predict(X_test)
        # predict_proba on the classifier step
        y_prob = full_pipeline.predict_proba(X_test)[:, 1]

        auc = roc_auc_score(y_test, y_prob)
        precision = precision_score(y_test, y_pred)
        recall = recall_score(y_test, y_pred)

        # Log parameters
        mlflow.log_param("n_estimators", n_estimators)
        mlflow.log_param("class_weight", class_weight)
        mlflow.log_param("max_samples", max_samples)
        mlflow.log_param("max_features", max_features)
        mlflow.log_param("max_depth", max_depth)
        

        # Log metrics
        mlflow.log_metric("roc_auc", auc)
        mlflow.log_metric("precision", precision)
        mlflow.log_metric("recall", recall)

        signature = infer_signature(X_train, full_pipeline.predict(X_train))

        # Register model
        mlflow.sklearn.log_model(
            full_pipeline,
            artifact_path="model",
            registered_model_name=MODEL_NAME,
            signature=signature,
            input_example=X_train.head(5)
        )

        print(f"ROC AUC: {auc}")

        client = MlflowClient()
        # Get all versions
        versions = client.search_model_versions(f"name='{MODEL_NAME}'")

        # Get highest version number
        latest_version = max(versions, key=lambda v: int(v.version))

        try:
            # Note: transitioning stages may raise errors on some MLflow setups
            # (file store YAML serialization). Catch and warn rather than fail.
           client.set_registered_model_alias(
                    name=MODEL_NAME,
                    alias="production",
                    version=latest_version.version
                )
           print(f"Model version {latest_version.version} promoted to Production.")
        except Exception as e:
            print("Warning: could not transition model version stage:", e)
            print(f"Model version {latest_version.version} registered (no stage transition).")


if __name__ == "__main__":
    train()