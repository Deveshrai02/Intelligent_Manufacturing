# ml/utils.py

import pandas as pd
from sqlalchemy import create_engine
from database.session import DATABASE_URL

def load_feature_data():
    engine = create_engine(DATABASE_URL)
    query = "SELECT * FROM vehicle_features;"
    df = pd.read_sql(query, engine)
    return df

def export_features_to_csv(path="vehicle_features.csv"):
    df = load_feature_data()
    df.to_csv(path, index=False)
    print(f"Exported dataset to {path}")