from ml.train_supervised import train as train_model
from ml.drift_monitor import detect_drift
from mlflow.tracking import MlflowClient

MODEL_NAME = "WarrantyModel"

def retrain_if_needed():

    if not detect_drift():
        print("No drift detected. Skipping retrain.")
        return

    print("Drift detected. Retraining model...")

    new_auc = train_model()

    client = MlflowClient()

    # Get production version
    mv = client.get_model_version_by_alias(MODEL_NAME, "production")
    prod_run = client.get_run(mv.run_id)
    prod_auc = prod_run.data.metrics.get("roc_auc")

    if new_auc > prod_auc:
        client.set_registered_model_alias(
            name=MODEL_NAME,
            alias="production",
            version=mv.version
        )
        print("New model promoted to production.")
    else:
        print("New model worse. Not promoted.")