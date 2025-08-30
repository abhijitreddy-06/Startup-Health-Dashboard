# src/etl/etl_pipeline.py (CLEAN, FINAL VERSION)
import pandas as pd
from sqlalchemy import create_engine
import os

# --- CONFIGURATION ---
# Make sure these match your database credentials
DB_USER = "postgres"
DB_PASSWORD = "Abhi.data"
DB_HOST = "localhost"
DB_PORT = "5432"
DB_NAME = "startup_dashboard_db"

DATABASE_URL = f"postgresql://{DB_USER}:{DB_PASSWORD}@{DB_HOST}:{DB_PORT}/{DB_NAME}"

RAW_DATA_PATH = "data/raw/gov-data-final.xlsx"
PROCESSED_DATA_PATH = "data/processed/cleaned_startups.csv"

def run_etl():
    """Runs the entire ETL process from start to finish."""
    print("Starting ETL process...")

    # --- 1. EXTRACTION ---
    try:
        df = pd.read_excel(RAW_DATA_PATH)
        print("Successfully extracted data from Excel file.")
    except FileNotFoundError:
        print(f"ERROR: The file was not found at {RAW_DATA_PATH}")
        return
    except Exception as e:
        print(f"An error occurred while reading the file: {e}")
        return

    # --- 2. TRANSFORMATION ---
    print("Transforming data...")
    # Clean column names based on your file's columns: ['S No.', 'Year', 'State', 'Industry', 'Count', 'Last Update']
    df.columns = df.columns.str.lower().str.replace(' ', '_').str.replace('.', '')
    
    # Select only the columns that match our database schema
    final_columns = ['year', 'state', 'industry', 'count', 'last_update']
    df_to_load = df[final_columns]
    
    print("Data transformation complete.")

    # Save the processed file for the ML model to use
    os.makedirs(os.path.dirname(PROCESSED_DATA_PATH), exist_ok=True)
    df_to_load.to_csv(PROCESSED_DATA_PATH, index=False)
    print(f"Cleaned data saved to {PROCESSED_DATA_PATH}")

    # --- 3. LOADING ---
    print("Loading data into PostgreSQL...")
    try:
        engine = create_engine(DATABASE_URL)
        # The 'if_exists='replace'' will drop the table first and then create it anew
        df_to_load.to_sql('startups', engine, if_exists='replace', index=False)
        print("✅ Data loaded successfully into 'startups' table.")
    except Exception as e:
        print(f"An error occurred while loading data to the database: {e}")

if __name__ == "__main__":
    run_etl()