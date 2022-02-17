from flask import Flask, request
import pickle 

app = Flask(__name__)

# load the compressed model
# health insurance expense predictor, linear regression,
# from dataset: https://www.kaggle.com/mirichoi0218/insurance
# read mode
# model = pickle.load(open('expense_model.pkl','rb')) 
with open('expense_model.pkl','rb') as output_file:
   model = pickle.load(output_file) 
   print("loaded the model")

# By default Flask uses get, same as
# @app.route('/', methods=['GET'])
@app.route('/')
def index():
    return "Hello, this is flask server welcome message."

# Make a prediction from GET params or POST body
# GET example: http://127.0.0.1:5000/prediction?age=29&bmi=35&children=0&sex=0&smoker=0&region=0
# POST example:
# {
#     "age": 29,
#     "bmi": 35,
#     "children": 0,
#     "sex": 0,
#     "smoker": 0,
#     "region": 0
# }
# inputs:
# age = 29
# bmi = 35
# children = 0
# sex = 0 # 'male'
# smoker = 0 # 'no'
# region = 0 # 'northeast'
# expect prediction = $7128.84
@app.route('/prediction', methods=['GET', 'POST'])
def predict():
    if request.method == 'GET':
        # print("made a GET request")
        # Try make a prediction from GET request query params
        # if key doesn't exist, returns None
        age = request.args.get('age')
        bmi = request.args.get('bmi')
        sex = request.args.get('sex')
        children = request.args.get('children')
        smoker = request.args.get('smoker')
        region = request.args.get('region')
        # get prediction
        input_cols = [[age, bmi, children, sex, smoker, region]]
        prediction = model.predict(input_cols)
        output = round(prediction[0], 2)
        # return "Your predicted annual health expense is ${}".format(output)
        return { 
            "message": "Your predicted annual health expense is ${}".format(output),
            "prediction": output
        }

    if request.method == 'POST':
        # print("made a POST")
        request_data = request.get_json()

        age = None
        bmi = None
        sex = None
        children = None
        smoker = None
        region = None

        if request_data:
            if 'age' in request_data:
                age = request_data['age']
            if 'bmi' in request_data:
                bmi = request_data['bmi']
            if 'sex' in request_data:
                sex = request_data['sex']
            if 'children' in request_data:
                children = request_data['children']
            if 'smoker' in request_data:
                smoker = request_data['smoker']
            if 'region' in request_data:
                region = request_data['region']
        print('request data', request_data)
            
        # get prediction
        input_cols = [[age, bmi, children, sex, smoker, region]]
        prediction = model.predict(input_cols)
        output = round(prediction[0], 2)
        return { 
            "message": "Your predicted annual health insurance expense is ${}".format(output),
            "prediction": output
        }

if __name__ == "__main__":
    app.run()