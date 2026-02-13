Relational DB Schema - 

VEHICLES

CREATE TABLE vehicles (
    vehicle_id UUID PRIMARY KEY,
    model_type VARCHAR(50),
    plant_id VARCHAR(50),
    production_date DATE,
    shift VARCHAR(10),
    created_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP
);

STATION OPERATIONS

CREATE TABLE station_operations (
    operation_id SERIAL PRIMARY KEY,
    vehicle_id UUID REFERENCES vehicles(vehicle_id),
    station_id VARCHAR(50),
    cycle_time FLOAT,
    error_count INT,
    rework_flag BOOLEAN,
    torque_value FLOAT,
    temperature FLOAT,
    operation_timestamp TIMESTAMP
);

VENDOR COMPONENTS

CREATE TABLE vendor_components (
    component_id SERIAL PRIMARY KEY,
    vehicle_id UUID REFERENCES vehicles(vehicle_id),
    component_type VARCHAR(50),
    vendor_id VARCHAR(50),
    batch_id VARCHAR(50),
    defect_flag BOOLEAN
);

WARRANTY CLAIMS

CREATE TABLE warranty_claims (
    claim_id SERIAL PRIMARY KEY,
    vehicle_id UUID REFERENCES vehicles(vehicle_id),
    warranty_flag BOOLEAN,
    claim_type VARCHAR(50),
    days_to_claim INT
);


Now we need an aggregated table to build the ML Model i.e,
One row for per prediction entity and structured feature vector
So an aggregated table with one to one relationship
New features -
1. Vehicle Id
2. Avg. Cycle Time
3. Total error count
4. Total count of torque value above specified limit 
5. Total count of temperature value above specified limit
6. Vendor Defect ratio
7. Rework Frequency






