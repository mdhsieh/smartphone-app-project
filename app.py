from flask import Flask, request
import pickle 

import pandas as pd
import numpy as np

from sklearn.preprocessing import OneHotEncoder
from sklearn.compose import ColumnTransformer

app = Flask(__name__)

# Load the pretrained model
# Housing price predictor, decision tree, training steps in notebook:
# house_price_model_cmpe_277.ipynb
# From dataset data_all_raw.csv: https://github.com/mboles01/Realestate 
with open('house_price_model.pkl','rb') as output_file:
   model = pickle.load(output_file) 
   print("loaded the model")

# # Load the pipeline of data transformations fitted on training dataset
# with open('house_price_pipeline.pkl','rb') as output_file:
#    pipeline = pickle.load(output_file) 
#    print("loaded the pipeline")


# By default Flask uses get, same as
# @app.route('/', methods=['GET'])
@app.route('/')
def index():
    return "Hello, this is flask server welcome message."

# Make a prediction from POST body
# POST example:
'''
{
    "home_size": 2220.0,
    "lot_size": 3999.0,
    "beds": 4,
    "baths": 2.0,
    "latitude": 37.521972,
    "longitude": -122.294079
}
'''
# inputs:
# home_size - float - size of house in square feet, must be < 5,000
# lot_size  - float - size of entire lot in square feet, must be < 2,0000
# beds - int - number of beds, must be < 6
# baths - float - number of baths, partial bath would be 0.5, must be < 6
# latitude - float - latitude of the house location
# longitude - float - longitude of the house location
# output: price - float - must be < 5,000,000
'''
{
    "message": "Your predicted housing price is $1736228.87",
    "prediction": 1736228.87,
    "rounded_prediction": 1736228.87
}
'''
@app.route('/prediction', methods=['POST'])
def predict():
    if request.method == 'POST':
        print("made a POST")
        request_data = request.get_json()

        home_size = None
        lot_size = None
        beds = None
        baths = None
        latitude = None
        longitude = None
        # city = None

        if request_data:
            if 'home_size' in request_data:
                home_size = request_data['home_size']
            if 'lot_size' in request_data:
                lot_size = request_data['lot_size']
            if 'beds' in request_data:
                beds = request_data['beds']
            if 'baths' in request_data:
                baths = request_data['baths']
            if 'latitude' in request_data:
                latitude = request_data['latitude']
            if 'longitude' in request_data:
                longitude = request_data['longitude']
            # if 'city' in request_data:
            #     city = request_data['city']
            
        # get prediction
        # input_cols = [[home_size, lot_size, beds, baths, latitude, longitude, city]]
        input_cols = [[home_size, lot_size, beds, baths, latitude, longitude]]
        input_df = pd.DataFrame(
            data=input_cols, 
            index=np.arange(len(input_cols)), 
            # columns=['Home_size', 'Lot_size', 'Beds', 'Baths', 'Latitude', 'Longitude', 'City']
            columns=['Home_size', 'Lot_size', 'Beds', 'Baths', 'Latitude', 'Longitude']
        )
        # prepared_data = pipeline.transform(input_df)
        # prediction = model.predict(prepared_data)
        prediction = model.predict(input_df)
        output = round(prediction[0], 2)
        return {
            "message": "Your predicted housing price is ${}".format(output),
            "prediction": prediction[0],
            "rounded_prediction": output
        }

if __name__ == "__main__":
    app.run()