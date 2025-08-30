# src/ml_service/model_train.py (MODIFIED FOR REGRESSION)

import pandas as pd
from sklearn.model_selection import train_test_split
# We use a Regressor to predict a number, not a Classifier
from sklearn.ensemble import RandomForestRegressor
from sklearn.metrics import mean_absolute_error
from sklearn.preprocessing import LabelEncoder
import joblib
import os

# --- CONFIGURATION ---
# This script will use the CSV you just uploaded.
PROCESSED_DATA_PATH = "data/processed/cleaned_startups.csv"
MODELS_DIR = "models"
MODEL_PATH = os.path.join(MODELS_DIR, "startup_model.pkl")
COLUMNS_PATH = os.path.join(MODELS_DIR, "model_columns.pkl")

def train_model():
    """Trains a regression model to predict startup count."""
    print("Starting model training (Regression to predict 'count')...")
    df = pd.read_csv(PROCESSED_DATA_PATH)

    # --- FEATURE ENGINEERING ---
    # The target is 'count'. Features are year, state, industry.
    features = ['year', 'state', 'industry']
    target = 'count'
    
    df_model = df[features + [target]].dropna()

    # Encode categorical features so the model can read them
    encoders = {}
    for col in ['state', 'industry']:
        le = LabelEncoder()
        df_model[col] = le.fit_transform(df_model[col])
        encoders[col] = le

    # Define X (features) and y (target)
    X = df_model[features]
    y = df_model[target]
    
    # --- MODEL TRAINING ---
    X_train, X_test, y_train, y_test = train_test_split(X, y, test_size=0.2, random_state=42)
    
    # Use the Regressor model
    model = RandomForestRegressor(n_estimators=100, random_state=42)
    model.fit(X_train, y_train)

    # --- EVALUATION ---
    preds = model.predict(X_test)
    mae = mean_absolute_error(y_test, preds)
    print(f"Model Mean Absolute Error: {mae:.2f}")

    # --- SAVING ---
    os.makedirs(MODELS_DIR, exist_ok=True)
    joblib.dump(model, MODEL_PATH)
    joblib.dump({'columns': list(X.columns), 'encoders': encoders}, COLUMNS_PATH)
    print(f"Regression model and columns saved to '{MODELS_DIR}' directory.")


if __name__ == "__main__":
    train_model()