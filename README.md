# 🚗 Intelligent Manufacturing --- Production-Grade Warranty Risk & Anomaly Detection Platform

**End-to-end ML system with model governance, drift detection, automated
retraining, and containerized deployment.**

------------------------------------------------------------------------

## 📌 Overview

Intelligent Manufacturing  is a full lifecycle Machine Learning platform designed to:

-   Predict vehicle warranty risk
-   Detect manufacturing anomalies
-   Monitor live feature drift
-   Automatically retrain when necessary
-   Promote better models safely via registry governance
-   Serve predictions via FastAPI
-   Log and monitor inference behavior

This project simulates a real automotive manufacturing analytics system
built using production-grade architecture principles.

------------------------------------------------------------------------

## 🏗 System Architecture

    Client
      │
      ▼
    FastAPI API
      - Strict schema validation
      - Risk engine
      - Inference logging
      │
      ▼
    MLflow Model Registry
      - Version tracking
      - Alias-based promotion
      - Model signature enforcement
      │
      ▼
    MySQL Database
      - Operational data
      - Feature tables
      - Prediction logs
      - Baseline statistics

------------------------------------------------------------------------

## 🔁 ML Lifecycle

### 1️⃣ Data Layer

-   Raw operational tables (vehicles, stations, vendors)
-   Feature aggregation into `vehicle_features`
-   Indexed and optimized queries

### 2️⃣ Model Training

-   Supervised model (RandomForest)
-   Anomaly detection model (IsolationForest)
-   Train/test split
-   MLflow experiment tracking
-   Model signature logging
-   Registry-based versioning
-   Alias-based production deployment

### 3️⃣ Serving Layer

-   FastAPI inference service
-   Strict Pydantic schema validation (`extra="forbid"`)
-   MLflow signature enforcement
-   Risk abstraction layer
-   Inference latency tracking
-   Prediction logging to database

### 4️⃣ Monitoring & Governance

-   Baseline feature statistics stored at training time
-   Rolling 24-hour drift detection
-   Z-score based statistical shift detection
-   Conditional retraining
-   Automatic alias promotion only if new model improves performance

### 5️⃣ Deployment

-   Dockerized API service
-   Dockerized MLflow server
-   Environment-driven configuration
-   Health check endpoint
-   Orchestrated via docker-compose

------------------------------------------------------------------------

## 📂 Repository Structure

    MIntel/
    │
    ├── api/
    │   ├── main.py
    │   ├── schemas.py
    │   ├── repository.py
    │
    ├── ml/
    │   ├── train_supervised.py
    │   ├── train_anomaly.py
    │   ├── drift_monitor.py
    │   ├── retrain.py
    │   ├── utils.py
    │
    ├── database/
    │   ├── models.py
    │   ├── session.py
    │
    ├── docker/
    │   ├── Dockerfile.api
    │   ├── Dockerfile.mlflow
    │
    ├── docker-compose.yml
    ├── requirements.txt
    └── README.md

------------------------------------------------------------------------

## 🚀 Running the System

### Start Services

    docker-compose up --build

Services started:

  Service   Port
  --------- ------
  API       8000
  MLflow    5000
  MySQL     3306

------------------------------------------------------------------------

### Train Models

    python -m ml.train_supervised
    python -m ml.train_anomaly

Models are: - Logged to MLflow - Registered - Assigned alias
`production`

------------------------------------------------------------------------

### Start API

    uvicorn api.main:app --reload

------------------------------------------------------------------------

### Example Prediction Request

    {
      "total_error_count": 3,
      "avg_cycle_time": 50.2,
      "cycle_time_variance": 3.1,
      "rework_ratio": 0.05,
      "vendor_defect_ratio": 0.1,
      "avg_torque": 98.4,
      "torque_deviation": 4.2
    }

Response:

    {
      "warranty_probability": 0.63,
      "anomaly_flag": 0,
      "risk_level": "MEDIUM"
    }

------------------------------------------------------------------------

## 📊 Drift Detection Logic

Drift is computed using:

-   Rolling 24-hour inference data
-   Baseline statistics stored at training time
-   Z-score threshold \> 3

```{=html}
<!-- -->
```
    z_score = |live_mean - baseline_mean| / baseline_std

If statistically significant: - Retraining is triggered

------------------------------------------------------------------------

## 🔁 Conditional Retraining

Retraining process:

1.  Detect drift
2.  Retrain new model
3.  Compare new ROC AUC with production
4.  Promote only if better

Prevents regression in live environment.

------------------------------------------------------------------------

## 🔐 Schema Enforcement

The system enforces:

-   Strict input schema via Pydantic
-   No extra fields allowed
-   MLflow model signature validation
-   Type enforcement at inference

Prevents prediction-time corruption.

------------------------------------------------------------------------

## 📈 Observability

Each prediction logs:

-   Model alias
-   Model version
-   Input payload
-   Probability
-   Risk level
-   Latency
-   Timestamp

Enables:

-   Canary comparison
-   Version performance monitoring
-   Auditability
-   Drift analysis

------------------------------------------------------------------------

## 🧠 Design Principles

-   Separation of concerns
-   Stateless serving
-   Registry-based governance
-   Safe alias promotion
-   Environment-driven configuration
-   Containerized reproducibility
-   Drift-aware lifecycle management

------------------------------------------------------------------------

## 🏁 Project Status

✅ End-to-end ML lifecycle implemented\
✅ Model governance and drift detection\
✅ Production-ready architecture\
✅ Containerized deployment

------------------------------------------------------------------------

**Author:** Devesh Kumar Rai\
Generated on: 2026-02-18
