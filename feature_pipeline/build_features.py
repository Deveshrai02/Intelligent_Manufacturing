# feature_pipeline/build_features.py

from database.session import SessionLocal
from sqlalchemy import text
from utils.logger import logger

def build_features():
    session = SessionLocal()
    logger.info("Starting feature aggregation...")

    # Clear existing feature table
    session.execute(text("DELETE FROM vehicle_features"))
    session.commit()

    aggregation_query = """
    INSERT INTO vehicle_features (
    vehicle_id,
    total_error_count,
    avg_cycle_time,
    cycle_time_variance,
    rework_ratio,
    vendor_defect_ratio,
    avg_torque,
    torque_deviation,
    warranty_flag
)

SELECT
    v.vehicle_id,
    s.total_error_count,
    s.avg_cycle_time,
    s.cycle_time_variance,
    s.rework_ratio,
    vc.vendor_defect_ratio,
    s.avg_torque,
    s.torque_deviation,
    wc.warranty_flag

FROM vehicles v

JOIN (
    SELECT
        vehicle_id,
        SUM(error_count) AS total_error_count,
        AVG(cycle_time) AS avg_cycle_time,
        VARIANCE(cycle_time) AS cycle_time_variance,
        AVG(rework_flag) AS rework_ratio,
        AVG(torque_value) AS avg_torque,
        STDDEV(torque_value) AS torque_deviation
    FROM station_operations
    GROUP BY vehicle_id
) s ON v.vehicle_id = s.vehicle_id

JOIN (
    SELECT
        vehicle_id,
        AVG(defect_flag) AS vendor_defect_ratio
    FROM vendor_components
    GROUP BY vehicle_id
) vc ON v.vehicle_id = vc.vehicle_id

JOIN warranty_claims wc ON v.vehicle_id = wc.vehicle_id;
    """

    session.execute(text(aggregation_query))
    session.commit()
    session.close()

    logger.info("Feature aggregation complete.")

if __name__ == "__main__":
    build_features()