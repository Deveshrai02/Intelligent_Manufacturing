import pandas as pd
from sqlalchemy import create_engine, text
from database.session import DATABASE_URL

engine = create_engine(DATABASE_URL)

def compute_live_stats():

    query = """
        SELECT request_payload
        FROM prediction_logs
        WHERE prediction_timestamp >= NOW() - INTERVAL 1 DAY
    """

    df = pd.read_sql(query, engine)

    if df.empty:
        print("No recent data.")
        return None

    # Expand JSON payload
    expanded = df["request_payload"].apply(pd.Series)

    live_stats = {}

    for col in expanded.columns:
        live_stats[col] = {
            "mean": expanded[col].mean(),
            "std": expanded[col].std()
        }

    return live_stats

def detect_drift(threshold_mean=0.3, threshold_std=0.5):

    live_stats = compute_live_stats()

    if not live_stats:
        return False

    baseline_query = "SELECT * FROM feature_baseline_stats"
    baseline_df = pd.read_sql(baseline_query, engine)

    drift_detected = False

    for _, row in baseline_df.iterrows():
        feature = row["feature_name"]

        if feature in live_stats:
            baseline_mean = row["mean_value"]
            live_mean = live_stats[feature]["mean"]
            baseline_std = row["std_value"]
            live_std = live_stats[feature]["std"]

            mean_change = abs(live_mean - baseline_mean) / (abs(baseline_mean) + 1e-6)
            std_change = abs(live_std - baseline_std) / (abs(baseline_std) + 1e-6)

            if mean_change > threshold_mean or std_change > threshold_std:
                drift_detected = True

    return drift_detected