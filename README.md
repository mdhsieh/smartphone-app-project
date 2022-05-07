### Machine Learning Mobile App

This is the machine learning backend of an Android app which uses machine learning to predict housing data for users. The [Android app itself is available here](https://github.com/eclewlow/house_price_estimator).
The model is hosted on Heroku and trained on [single-family house data](https://github.com/mboles01/Realestate) in the San Francisco Bay Area from June 2019.

### Development Instructions - Frontend
Make a POST request to model hosted on Heroku with URL:
```
https://machine-learning-mobile-app.herokuapp.com/prediction
```
An example request JSON body is:
```
{
    "home_size": 2220.0,
    "lot_size": 3999.0,
    "beds": 4,
    "baths": 2.0,
    "latitude": 37.521972,
    "longitude": -122.294079
}
```
Or follow Backend instructions below to test the model locally.

### Development Instructions - Backend
You can create a virtual environment by downloading [Miniconda](https://docs.conda.io/en/latest/miniconda.html) and install required dependencies in the environment, e.g.
```
conda create --name flask
conda install pip
```
Python version tested was 3.9.7.

Install dependencies:
`conda activate flask`
`pip install -r requirements.txt`

Run the app locally to e.g. test a POST prediction request:
`flask run`

You can check if POST requests work by installing [Postman](https://www.postman.com/).
Fill in the URL, e.g. `http://127.0.0.1:5000/prediction`. Go to Body->raw and in dropdown pick JSON. Then put in the example request JSON body and hit Send to see the response.

The response should be similar to the following:
```
{
    "message": "Your predicted housing price is $1736228.87",
    "prediction": 1736228.87,
    "rounded_prediction": 1736228.87
}
```

### Development Instructions - Backend Model Training
The Colab notebook used for training and testing is `house_price_model_cmpe_277.ipynb`.

Install [Heroku CLI](https://devcenter.heroku.com/articles/heroku-cli) to login and make changes to the server hosting the model, e.g. you want to retrain and upload an updated model. These instructions are for MacOS but for Windows use the installer as instructed in the article.
`brew tap heroku/brew && brew install heroku`
`heroku login`

You have to get access to the Heroku project to make changes. Push changes to Heroku:
`git push heroku master`

Push changes to this repo itself:
`git push`