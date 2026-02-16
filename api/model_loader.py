import mlflow.pyfunc

WARRANTY_MODEL_URI = "models:/WarrantyModel@production"
ANOMALY_MODEL_URI = "models:/AnomalyModel@production"

def load_models():
    warranty_model = mlflow.pyfunc.load_model(WARRANTY_MODEL_URI)
    anomaly_model = mlflow.pyfunc.load_model(ANOMALY_MODEL_URI)
    return warranty_model, anomaly_model