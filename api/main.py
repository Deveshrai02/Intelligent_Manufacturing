from fastapi import FastAPI
from pydantic import BaseModel
import pandas as pd
from fastapi import HTTPException

from api.model_loader import load_models
from api.risk_engine import calculate_risk

app = FastAPI(title="AI Powered Manufacturing Platform")

# Load models once at startup (important)
warranty_model, anomaly_model = load_models()


class VehicleInput(BaseModel):
    total_error_count: int
    avg_cycle_time: float
    cycle_time_variance: float
    rework_ratio: float
    vendor_defect_ratio: float
    avg_torque: float
    torque_deviation: float

@app.get("/")
def root():
    return {"message": "Welcome to the AI Powered Manufacturing Platform API!"}

@app.get("/health")
def health():
    return {"status": "healthy"}


@app.post("/predict")
def predict(vehicle: VehicleInput):

    input_df = pd.DataFrame([vehicle.model_dump()])
    try:
        # Warranty model outputs probability
        warranty_prob = warranty_model.predict(input_df)[0]

        # IsolationForest returns -1 (anomaly) or 1 (normal)
        anomaly_flag = anomaly_model.predict(input_df)[0]

    except Exception as e:
        raise HTTPException(status_code=500, detail=f"Error during prediction: {str(e)}")

    risk = calculate_risk(warranty_prob, anomaly_flag)

    return {
        "warranty_probability": float(warranty_prob),
        "anomaly_flag": int(anomaly_flag),
        "risk_level": risk
    }