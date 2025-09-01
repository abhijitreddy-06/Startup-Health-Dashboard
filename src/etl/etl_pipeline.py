import pandas as pd
from sqlalchemy import create_engine
import os
from dotenv import load_dotenv

load_dotenv()

DB_USER = os.getenv("DB_USER", "postgres")
DB_PASSWORD = os.getenv("DB_PASSWORD", "")
DB_HOST = os.getenv("DB_HOST", "localhost")
DB_PORT = os.getenv("DB_PORT", "5432")
DB_NAME = os.getenv("DB_NAME", "startup_dashboard_db")

DATABASE_URL = f"postgresql://{DB_USER}:{DB_PASSWORD}@{DB_HOST}:{DB_PORT}/{DB_NAME}"

RAW_DATA_PATH = "data/raw/gov-data-final.xlsx"
PROCESSED_DATA_PATH = "data/processed/cleaned_startups.csv"

def run_etl():
    print("Starting ETL process...")
    try:
        df = pd.read_excel(RAW_DATA_PATH)
        print("Successfully extracted data from Excel file.")
    except FileNotFoundError:
        print(f"ERROR: The file was not found at {RAW_DATA_PATH}")
        return
    except Exception as e:
        print(f"An error occurred while reading the file: {e}")
        return

    print("Transforming data...")
    df.columns = df.columns.str.lower().str.replace(' ', '_').str.replace('.', '')
    final_columns = ['year', 'state', 'industry', 'count', 'last_update']
    df_to_load = df[final_columns]
    print("Data transformation complete.")

    os.makedirs(os.path.dirname(PROCESSED_DATA_PATH), exist_ok=True)
    df_to_load.to_csv(PROCESSED_DATA_PATH, index=False)
    print(f"Cleaned data saved to {PROCESSED_DATA_PATH}")

    print("Loading data into PostgreSQL...")
    try:
        engine = create_engine(DATABASE_URL)
        df_to_load.to_sql('startups', engine, if_exists='replace', index=False)
        print("Data loaded successfully into 'startups' table.")
    except Exception as e:
        print(f"An error occurred while loading data to the database: {e}")

if __name__ == "__main__":
    run_etl()
