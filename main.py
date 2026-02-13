# main.py

from database.session import SessionLocal
from database.models import Vehicle
import uuid
import datetime

session = SessionLocal()

new_vehicle = Vehicle(
    vehicle_id=str(uuid.uuid4()),
    model_type="SUV",
    plant_id="Plant_A",
    production_date=datetime.date.today(),
    shift="Morning"
)

session.add(new_vehicle)
session.commit()

# Query back
vehicles = session.query(Vehicle).all()

for v in vehicles:
    print(v.vehicle_id, v.model_type)

session.close()