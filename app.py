from flask import Flask, request
import pickle 

app = Flask(__name__)

# load the compressed model
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

# Try make a prediction from get request query params
@app.route('/prediction', methods=['GET', 'POST'])
def predict():
    if request.method == 'GET':
        print("made a GET request")
        # example: http://127.0.0.1:5000/prediction?age=29&bmi=35&children=0&sex=0&smoker=0&region=0
        # age = 29
        # bmi = 35
        # children = 0
        # Sex = 0 # 'male'
        # Smoker = 0 # 'no'
        # Region = 0 # 'northeast'
        # expect prediction = $7128.84

        # if key doesn't exist, returns None
        age = request.args.get('age')
        bmi = request.args.get('bmi')
        sex = request.args.get('sex')
        children = request.args.get('children')
        smoker = request.args.get('smoker')
        region = request.args.get('region')
        # get prediction
        input_cols = [[age, bmi, children, sex, smoker, region]]
        print(input_cols)
        prediction = model.predict(input_cols)
        output = round(prediction[0], 2)
        return "Your predicted annual health expense is $ {}".format(output)

if __name__ == "__main__":
    app.run()