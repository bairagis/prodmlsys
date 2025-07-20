# call fask REST API ruunning on localhost:5002
import requests 
def call_predict_api(flightType, agency, distance, time):
    url = 'http://localhost:5002/predict'
    data = {
    'distance': 1000,
    'time': 2,        
    'flightType': 'premium',  # valid: 'premium', 'firstClass', 'economic'
    'agency': 'Rainbow'
    }
    
    response = requests.post(url, json=data)
    
    if response.status_code == 200:
        return response.json()['predicted_price']
    else:
        raise Exception(f"API call failed with status code {response.status_code}: {response.text}")
    

print("The predicted price returned from API: ", call_predict_api(['premium'],['Rainbow'] ,[1000],[2]))