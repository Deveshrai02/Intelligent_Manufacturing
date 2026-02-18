from fastapi import FastAPI
from pydantic import BaseModel, ConfigDict
import pandas as pd
from fastapi import HTTPException

from api.model_loader import load_models , get_model_version
from api.risk_engine import calculate_risk

import time
import json
from sqlalchemy import create_engine
from database.session import DATABASE_URL
from sqlalchemy import text

app = FastAPI(title="AI Powered Manufacturing Platform")

# Load models once at startup (important)
warranty_model, anomaly_model = load_models()

engine = create_engine(DATABASE_URL)


class VehicleInput(BaseModel):
    total_error_count: int
    avg_cycle_time: float
    cycle_time_variance: float
    rework_ratio: float
    vendor_defect_ratio: float
    avg_torque: float
    torque_deviation: float

    model_config = ConfigDict(extra="forbid")

@app.get("/")
def root():
    return {"message": "Welcome to the AI Powered Manufacturing Platform API!"}

@app.get("/health")
def health():
    return {"status": "healthy"}


@app.post("/predict")
def predict(vehicle: VehicleInput):

    start_time = time.time()

    input_df = pd.DataFrame([vehicle.model_dump()])

    warranty_prob = warranty_model.predict(input_df)[0]
    anomaly_flag = anomaly_model.predict(input_df)[0]

    risk = calculate_risk(warranty_prob, anomaly_flag)

    latency = (time.time() - start_time) * 1000

    # Fetch model versions
    warranty_version = get_model_version("WarrantyModel")
    anomaly_version = get_model_version("AnomalyModel")

    print("Reached logging block")

    # Insert log
    insert_query = text("""
    INSERT INTO prediction_logs
    (model_alias, model_version, warranty_probability,
     anomaly_flag, risk_level, request_payload, latency_ms)
    VALUES
    (:model_alias, :model_version, :warranty_probability,
     :anomaly_flag, :risk_level, :request_payload, :latency_ms)
    """)

    with engine.begin() as conn:
        print("Inside transaction")
        print("Connected DB:", conn.execute(text("SELECT DATABASE();")).fetchone())
        result =conn.execute(
        insert_query,
        {
            "model_alias": "production",
            "model_version": warranty_version,
            "warranty_probability": float(warranty_prob),
            "anomaly_flag": int(anomaly_flag),
            "risk_level": risk,
            "request_payload": json.dumps(vehicle.model_dump()),
            "latency_ms": latency
        })
        print("Rows inserted:", result.rowcount)
        
      

    return {
        "warranty_probability": float(warranty_prob),
        "anomaly_flag": int(anomaly_flag),
        "risk_level": risk,
        "latency_ms": latency
    }