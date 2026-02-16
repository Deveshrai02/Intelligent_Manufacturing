import mlflow
import mlflow.sklearn
from mlflow.tracking import MlflowClient
from sklearn.ensemble import IsolationForest
from sklearn.preprocessing import StandardScaler
from sklearn.pipeline import Pipeline
from ml.utils import load_feature_data
import numpy as np
from sklearn.compose import ColumnTransformer
from sklearn.preprocessing import PowerTransformer, FunctionTransformer, OneHotEncoder
from pandas.api.types import is_numeric_dtype
from mlflow.models import infer_signature

MODEL_NAME = "AnomalyModel"


def train():

    mlflow.set_tracking_uri("file:./mlruns")
    mlflow.set_experiment("Anomaly_Detection")

    df = load_feature_data().dropna()

    X = df.drop(["vehicle_id", "warranty_flag", "feature_snapshot_timestamp" , "data_version"], axis=1)
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

    with mlflow.start_run():

        contamination = 0.05

        model = IsolationForest(
            n_estimators=100,
            contamination=contamination,
            random_state=42
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


        pipeline = Pipeline([
            ("preprocessor", preprocessor),
            ("model", model)
        ])

        pipeline.fit(X)

        mlflow.log_param("contamination", contamination)
        mlflow.log_param("model_type", "IsolationForest")

        signature = infer_signature(X, pipeline.predict(X))

        mlflow.sklearn.log_model(
            pipeline,
            artifact_path="model",
            registered_model_name=MODEL_NAME,
            signature=signature,
            input_example=X.head(5)
        )

        client = MlflowClient()

        # Get all versions
        versions = client.search_model_versions(f"name='{MODEL_NAME}'")

        #  Get highest version number
        latest_version = max(versions, key=lambda v: int(v.version))

        # Assign alias
        client.set_registered_model_alias(
            name=MODEL_NAME,
            alias="production",
            version=latest_version.version
        )
        print(f"Anomaly model version {latest_version.version} promoted to Production.")


if __name__ == "__main__":
    train()