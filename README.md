### Machine Learning Mobile App

This is a React Native app which uses machine learning to predict housing data for users.
The model is hosted on Heroku and trained on [single-family house data](https://github.com/mboles01/Realestate) in the San Francisco Bay Area from June 2019.

### Development Instructions - Frontend
First install [Node.js](https://docs.npmjs.com/downloading-and-installing-node-js-and-npm) and NPM if haven't already. 
Then install React Native using [Expo CLI](https://archive.reactnative.dev/docs/getting-started).
The frontend is in a Expo project folder called `house-price-estimator`.
```
cd house-price-estimator
npm install
npm start
```
Make a POST request to model hosted on Heroku with URL:
```
https://machine-learning-mobile-app.herokuapp.com/prediction
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
`pip install -r requirements.txt`

Run the app locally to e.g. test a POST prediction request:
`flask run`

You can check if POST requests work by installing [Postman](https://www.postman.com/).
Fill in the URL, e.g. `http://127.0.0.1:5000/prediction`. Go to Body->raw and in dropdown pick JSON. Then put in the request JSON body and hit Send to see the response. An example request is in `app.py` comments.

Install [Heroku CLI](https://devcenter.heroku.com/articles/heroku-cli) to login and make changes to the server hosting the model, e.g. you want to retrain and upload an updated model. These instructions are for MacOS but for Windows use the installer as instructed in the article.
`brew tap heroku/brew && brew install heroku`
`heroku login`

You have to get access to the Heroku project to make changes. Push changes to Heroku:
`git push heroku master`

Push changes to this repo itself:
`git push`