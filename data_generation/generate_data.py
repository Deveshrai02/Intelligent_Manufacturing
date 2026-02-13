# data_generation/generate_data.py

import uuid
import random
import datetime
from database.session import SessionLocal
from database.models import Vehicle, StationOperation, VendorComponent, WarrantyClaim
from utils.logger import logger

NUM_VEHICLES = 5000
NUM_STATIONS = 25

VENDORS = ["Xelix", "Neon", "Physher"]
VENDOR_DEFECT_PROB = {
    "Xelix": 0.03,
    "Neon": 0.08,  # Riskier vendor
    "Physher": 0.01
}

def generate_vehicle():
    return {
        "vehicle_id": str(uuid.uuid4()),
        "model_type": random.choice(["SUV", "Sedan", "Truck"]),
        "plant_id": random.choice(["Plant_A", "Plant_B"]),
        "production_date": datetime.date.today() - datetime.timedelta(days=random.randint(0, 365)),
        "shift": random.choice(["Morning", "Evening", "Night"])
    }

def generate_station_data(vehicle_id, high_risk=False):
    operations = []
    for i in range(NUM_STATIONS):
        base_cycle = random.uniform(40, 60)

        # Inject anomaly
        if high_risk and random.random() < 0.3:
            base_cycle *= random.uniform(1.2, 1.5)

        operation = StationOperation(
            vehicle_id=vehicle_id,
            station_id=f"Station_{i+1}",
            cycle_time=base_cycle,
            error_count=random.randint(0, 3) if not high_risk else random.randint(1, 5),
            rework_flag=random.random() < 0.1 if not high_risk else random.random() < 0.3,
            torque_value=random.uniform(90, 110) if not high_risk else random.uniform(80, 130),
            temperature=random.uniform(20, 40),
            operation_timestamp=datetime.datetime.now()
        )

        operations.append(operation)
    return operations

def generate_vendor_data(vehicle_id):
    components = []
    for comp in ["Engine", "Transmission", "Brake"]:
        vendor = random.choice(VENDORS)
        defect = random.random() < VENDOR_DEFECT_PROB[vendor]

        components.append(
            VendorComponent(
                vehicle_id=vehicle_id,
                component_type=comp,
                vendor_id=vendor,
                batch_id=f"BATCH_{random.randint(1000,9999)}",
                defect_flag=defect
            )
        )
    return components

def generate_warranty(vehicle_id, high_risk):
    warranty_flag = False

    if high_risk:
        warranty_flag = random.random() < 0.4
    else:
        warranty_flag = random.random() < 0.05

    return WarrantyClaim(
        vehicle_id=vehicle_id,
        warranty_flag=warranty_flag,
        claim_type="Mechanical" if warranty_flag else None,
        days_to_claim=random.randint(30, 365) if warranty_flag else None
    )

def main():
    session = SessionLocal()
    logger.info("Starting synthetic data generation...")

    for i in range(NUM_VEHICLES):
        high_risk = random.random() < 0.05  # 5% risky vehicles

        vehicle_data = generate_vehicle()
        vehicle = Vehicle(**vehicle_data)

        session.add(vehicle)

        station_ops = generate_station_data(vehicle.vehicle_id, high_risk)
        for op in station_ops:
            session.add(op)

        vendor_data = generate_vendor_data(vehicle.vehicle_id)
        for comp in vendor_data:
            session.add(comp)

        warranty = generate_warranty(vehicle.vehicle_id, high_risk)
        session.add(warranty)

        if i % 500 == 0:
            logger.info(f"Inserted {i} vehicles...")
            session.commit()

    session.commit()
    session.close()
    logger.info("Data generation complete.")

if __name__ == "__main__":
    main()