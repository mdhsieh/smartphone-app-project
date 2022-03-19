from flask import Flask, request
import pickle 

import pandas as pd
import numpy as np

app = Flask(__name__)

# load the pickle model
# housing price predictor, linear regression,
# from dataset: https://github.com/mboles01/Realestate 
# read mode
with open('house_price_model.pkl','rb') as output_file:
   model = pickle.load(output_file) 
   print("loaded the model")

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
    "baths": 2.0
}
'''
# inputs:
# home_size - float - size of house in square feet, must be < 5000
# lot_size  - float - size of entire lot in square feet, must be < 20000
# beds - int - number of beds, must be < 6
# baths = - float - number of baths, partial bath would be 0.5, must be < 6
# output: price - float - must be < 5000000
'''
{
    "message": "Your predicted housing price is $1595000.0",
    "prediction": 1595000.0
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

        if request_data:
            if 'home_size' in request_data:
                home_size = request_data['home_size']
            if 'lot_size' in request_data:
                lot_size = request_data['lot_size']
            if 'beds' in request_data:
                beds = request_data['beds']
            if 'baths' in request_data:
                baths = request_data['baths']
            
        # # get prediction
        input_cols = [[home_size, lot_size, beds, baths]]
        prediction = model.predict(input_cols)
        output = round(prediction[0], 2)
        return {
            "message": "Your predicted housing price is ${}".format(output),
            "prediction": prediction[0]
        }

if __name__ == "__main__":
    app.run()