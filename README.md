### Machine Learning Mobile App

This is a React Native app which uses machine learning to predict housing data for users.
The model is hosted on Heroku and trained on [single-family house data]() in the San Francisco Bay Area from June 2019.


### Development Instructions
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
Fill in the URL, e.g. `http://127.0.0.1:5000/prediction`. Go to Body->raw and in dropdown pick JSON. Then put in the example request JSON body and hit Send to see the response.

Install [Heroku CLI](https://devcenter.heroku.com/articles/heroku-cli) to login and make changes to the server hosting the model, e.g. you want to retrain and upload an updated model. These instructions are for MacOS but for Windows use the installer as instructed in the article.
`brew tap heroku/brew && brew install heroku`
`heroku login`

You have to get access to the Heroku project to make changes. Push changes to Heroku:
`git push heroku master`

Push changes to this repo itself:
`git push`