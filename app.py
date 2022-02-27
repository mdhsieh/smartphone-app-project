from flask import Flask, request
import pickle 

import pandas as pd
import numpy as np
from sklearn.preprocessing import OneHotEncoder
from sklearn.impute import SimpleImputer
from sklearn.model_selection import StratifiedShuffleSplit
from sklearn.pipeline import Pipeline
from sklearn.preprocessing import StandardScaler
from sklearn.compose import ColumnTransformer

app = Flask(__name__)

def get_housing_dataset(filepath):
    df = pd.read_csv(filepath)
    print("loaded housing dataset")
    df["income_cat"] = pd.cut(df["median_income"], bins = [0 , 1.5 , 3.0 , 4.5 , 6 , np.inf], labels=[1 , 2 , 3 , 4 , 5])
    split = StratifiedShuffleSplit(n_splits= 1 , test_size= 0.2 , random_state=42)
    for train_index, test_index in split.split(df, df["income_cat"]):
        strat_train_set = df.loc[train_index]
        strat_test_set = df.loc[test_index]
    for set_ in (strat_test_set , strat_train_set):
        set_.drop("income_cat" , axis = 1 ,  inplace = True)
    housing = strat_train_set.drop("median_house_value" ,axis = 1)
    return housing

def build_pipeline():
    housing = get_housing_dataset("housing.csv")
    housing_num = housing.drop("ocean_proximity", axis=1)
    print("got housing set with only numerical values:")
    print(housing_num.head())

    num_pipeline = Pipeline([
    ('imputer', SimpleImputer(strategy="median")),
    ('std_scaler', StandardScaler()),
    ])
    # housing_num_tr = num_pipeline.fit_transform(housing_num)

    num_attribs = list(housing_num)
    cat_attribs = ["ocean_proximity"]

    full_pipeline = ColumnTransformer([
    ("num", num_pipeline, num_attribs),
    ("cat", OneHotEncoder(), cat_attribs),
    ])
    housing_prepared = full_pipeline.fit_transform(housing)
    print("built pipeline")
    return full_pipeline

# load the pickle model
# housing price predictor, linear regression,
# from dataset: https://www.kaggle.com/camnugent/california-housing-prices
# trained from notebook: https://www.kaggle.com/aakashjoshi123/o-reilly-solution-with-my-observations-notebook
# read mode
with open('housing_price_model.pkl','rb') as output_file:
   model = pickle.load(output_file) 
   print("loaded the model")

# pipeline = build_pipeline()
with open('housing_dataset_pipeline.pkl','rb') as output_file:
   pipeline = pickle.load(output_file) 
   print("loaded the pipeline")

# By default Flask uses get, same as
# @app.route('/', methods=['GET'])
@app.route('/')
def index():
    return "Hello, this is flask server welcome message."

# Make a prediction from POST body
# POST example:
'''
{
    "longitude": -121.89,
    "latitude": 37.29,
    "housing_median_age": 38.0,
    "total_rooms": 1568.0,
    "total_bedrooms": 351.0,                       
    "population": 710.0,
    "households": 339.0,
    "median_income": 2.7042,
    "ocean_proximity": "<1H OCEAN"
}
'''
# inputs:
# longitude = -121.89 
# latitude  =  37.29 
# housing_median_age  = 38.0  
# total_rooms = 1568.0  
# total_bedrooms  = 351.0                         
# population = 710.0 
# households = 339.0 
# median_income = 2.7042 
# ocean_proximity =  '<1H OCEAN'
# expected output = 211574.39523833
@app.route('/prediction', methods=['POST'])
def predict():
    if request.method == 'POST':
        print("made a POST")
        request_data = request.get_json()

        longitude = None
        latitude = None
        housing_median_age = None
        total_rooms = None
        total_bedrooms = None
        population = None
        households = None
        median_income = None
        ocean_proximity = None

        if request_data:
            if 'longitude' in request_data:
                longitude = request_data['longitude']
            if 'latitude' in request_data:
                latitude = request_data['latitude']
            if 'housing_median_age' in request_data:
                housing_median_age = request_data['housing_median_age']
            if 'total_rooms' in request_data:
                total_rooms = request_data['total_rooms']
            if 'total_bedrooms' in request_data:
                total_bedrooms = request_data['total_bedrooms']
            if 'population' in request_data:
                population = request_data['population']
            if 'households' in request_data:
                households = request_data['households']
            if 'median_income' in request_data:
                median_income = request_data['median_income']
            if 'ocean_proximity' in request_data:
                ocean_proximity = request_data['ocean_proximity']
        # print('request data', request_data)
            
        # # get prediction
        input_cols = [[longitude, latitude, housing_median_age, total_rooms, total_bedrooms, population, households, median_income, ocean_proximity]]
        input_df = pd.DataFrame(
            data=input_cols, 
            index=np.arange(len(input_cols)), 
            columns=["longitude", "latitude", "housing_median_age", "total_rooms", 
            "total_bedrooms", "population", "households", "median_income", "ocean_proximity"]
        )
        prepared_data = pipeline.transform(input_df)
        prediction = model.predict(prepared_data)
        # prediction = model.predict(input_cols)
        output = round(prediction[0], 2)
        return {
            "message": "Your predicted housing price is ${}".format(output),
            "prediction": prediction[0]
        }

if __name__ == "__main__":
    app.run()