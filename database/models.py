# database/models.py

from sqlalchemy import Column, String, Float, Integer, Boolean, Date, DateTime, ForeignKey
from sqlalchemy.orm import declarative_base
import datetime

Base = declarative_base()

class Vehicle(Base):
    __tablename__ = "vehicles"

    vehicle_id = Column(String(36), primary_key=True)
    model_type = Column(String(50))
    plant_id = Column(String(50))
    production_date = Column(Date)
    shift = Column(String(10))
    created_at = Column(DateTime, default=datetime.datetime.utcnow)


class StationOperation(Base):
    __tablename__ = "station_operations"

    operation_id = Column(Integer, primary_key=True, autoincrement=True)
    vehicle_id = Column(String(36), ForeignKey("vehicles.vehicle_id"))
    station_id = Column(String(50))
    cycle_time = Column(Float)
    error_count = Column(Integer)
    rework_flag = Column(Boolean)
    torque_value = Column(Float)
    temperature = Column(Float)
    operation_timestamp = Column(DateTime)


class VendorComponent(Base):
    __tablename__ = "vendor_components"

    component_id = Column(Integer, primary_key=True, autoincrement=True)
    vehicle_id = Column(String(36), ForeignKey("vehicles.vehicle_id"))
    component_type = Column(String(50))
    vendor_id = Column(String(50))
    batch_id = Column(String(50))
    defect_flag = Column(Boolean)


class WarrantyClaim(Base):
    __tablename__ = "warranty_claims"

    claim_id = Column(Integer, primary_key=True, autoincrement=True)
    vehicle_id = Column(String(36), ForeignKey("vehicles.vehicle_id"))
    warranty_flag = Column(Boolean)
    claim_type = Column(String(50))
    days_to_claim = Column(Integer)