# Define a function for Flask app that take flightType, agency, distance, time as input and return the predicted price
import joblib
from flask import Flask, request, jsonify
import pandas as pd

def predict_flight_price(flightType, agency, distance, time):
    # Create a DataFrame for the input data
    input_data = pd.DataFrame({
        'flightType': [flightType],
        'agency': [agency],
        'distance': [distance],
        'time': [time]
    })
   
    print("inside the predict")
    
    # load encoders and model
    flightType_encoder = joblib.load('model/flightType_encoder.pkl')
    agency_encoder = joblib.load('model/agency_encoder.pkl')
    rf_model_best = joblib.load('model/rf_model_best.pkl')
    
    # Encode the categorical features
    input_data['flightType_encoded'] = flightType_encoder.transform(input_data['flightType'])
    input_data['agency_encoded'] = agency_encoder.transform(input_data['agency'])
    
    # Drop the original categorical columns
    input_data = input_data.drop(['flightType', 'agency'], axis=1)
    
    # Predict the price using the loaded model
    predicted_price = rf_model_best.predict(input_data)

    print("Predicted data: ", predicted_price)
    
    return predicted_price[0]  # Return the predicted price



app = Flask(__name__)
@app.route('/predict', methods=['POST'])
def predict():
    data = request.get_json()
    flightType = data['flightType']
    agency = data['agency']
    distance = data['distance']
    time = data['time']
    
 # print request data   
    print(data)
    print(flightType)
    print(agency)
    print(distance)
    print(time)


    # Call the prediction function
    predicted_price = predict_flight_price(flightType, agency, distance, time)
    
    
    return jsonify({'predicted_price': predicted_price})


# call the Flask Rest API
if __name__ == '__main__':
    app.run(debug=True, host='0.0.0.0', port=5002)
