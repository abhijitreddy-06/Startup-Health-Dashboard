
from flask import Flask, request, jsonify
import joblib
import pandas as pd

app = Flask(__name__)


model = joblib.load('../../models/startup_model.pkl')
preprocessors = joblib.load('../../models/model_columns.pkl')
model_columns = preprocessors['columns']
label_encoders = preprocessors['encoders']

@app.route('/predict', methods=['POST'])
def predict():
    try:
        json_data = request.get_json()
     
        data = pd.DataFrame(json_data, index=[0])

        for col, le in label_encoders.items():
         
            data[col] = data[col].apply(lambda x: x if x in le.classes_ else le.classes_[0])
            data[col] = le.transform(data[col])

        query = data[model_columns]
        prediction = model.predict(query)[0]
        return jsonify({'predicted_count': round(prediction, 2)})

    except Exception as e:
    
        print(f"AN ERROR OCCURRED: {e}") 
        return jsonify({'error': str(e)}), 500

if __name__ == '__main__':
    app.run(port=5001, debug=True)