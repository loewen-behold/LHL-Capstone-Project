from flask import Flask, request, jsonify
import pandas as pd
import numpy as np
import joblib
from pre_predict_processing import add_eng_values_pre_predict, alter_term_gender_pre_predict

app = Flask(__name__)

# Load the saved model
model = joblib.load('../models/voting_classifier_best_model2.pkl')

# Define the preprocessing function
def preprocess_data(data):

    # Drop unnecessary columns
    data.drop('pseudo_id', axis=1, inplace=True)

    # Add engineered values
    data = add_eng_values_pre_predict(data)

    # Alter categorical columns
    data = alter_term_gender_pre_predict(data)

    return data

@app.route('/predict', methods=['POST'])
def predict():
    try:
        # Retrieve data from the request
        data = request.json
        
        # Create a DataFrame from the input data
        input_df = pd.DataFrame([data])
        
        # Preprocess the data
        preprocessed_data = preprocess_data(input_df)
        preprocessed_data.to_csv('../data/processed_data/df_preprediction_data.csv', index=False)
        # Make predictions using the loaded model
        prediction = model.predict(preprocessed_data)

        # Return the prediction as JSON
        return jsonify({'prediction': int(prediction[0])})

    except Exception as e:
        return jsonify({'error': str(e)})

if __name__ == '__main__':
    app.run(port=5000)