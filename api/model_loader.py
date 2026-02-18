import mlflow.pyfunc
from mlflow.tracking import MlflowClient

WARRANTY_MODEL_URI = "models:/WarrantyModel@production"
ANOMALY_MODEL_URI = "models:/AnomalyModel@production"

def load_models():
    warranty_model = mlflow.pyfunc.load_model(WARRANTY_MODEL_URI)
    anomaly_model = mlflow.pyfunc.load_model(ANOMALY_MODEL_URI)
    return warranty_model, anomaly_model



client = MlflowClient()

def get_model_version(model_name, alias="production"):
    mv = client.get_model_version_by_alias(model_name, alias)
    return mv.version