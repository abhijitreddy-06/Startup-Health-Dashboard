# src/ml_service/app.py
from flask import Flask, request, jsonify
import joblib
import pandas as pd

app = Flask(__name__)

# Load the model and preprocessing objects
model = joblib.load('../../models/startup_model.pkl')
preprocessors = joblib.load('../../models/model_columns.pkl')
model_columns = preprocessors['columns']
label_encoders = preprocessors['encoders']

@app.route('/predict', methods=['POST'])
def predict():
    try:
        json_data = request.get_json()
        # Create a DataFrame from the incoming JSON
        data = pd.DataFrame(json_data, index=[0])

        # Preprocess the data just like the training data
        for col, le in label_encoders.items():
            # Use a default value for unseen labels, or handle error
            data[col] = data[col].apply(lambda x: x if x in le.classes_ else le.classes_[0])
            data[col] = le.transform(data[col])

        # Ensure columns are in the same order as during training
        query = data[model_columns]
        prediction = model.predict(query)[0]
        return jsonify({'predicted_count': round(prediction, 2)})

    except Exception as e:
        # ADD THIS LINE TO SEE THE ERROR IN THE TERMINAL
        print(f"AN ERROR OCCURRED: {e}") 
        return jsonify({'error': str(e)}), 500

if __name__ == '__main__':
    # Run on a different port than your Express API, e.g., 5001
    app.run(port=5001, debug=True)