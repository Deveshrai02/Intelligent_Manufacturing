import pandas as pd
from sqlalchemy import create_engine
from database.session import DATABASE_URL


def load_feature_data(data_version=None):
    """
    Loads feature snapshot from vehicle_features table.
    Optionally filter by data_version.
    """

    engine = create_engine(DATABASE_URL)

    if data_version:
        query = f"""
        SELECT * FROM vehicle_features
        WHERE data_version = '{data_version}'
        """
    else:
        query = "SELECT * FROM vehicle_features"

    df = pd.read_sql(query, engine)

    return df