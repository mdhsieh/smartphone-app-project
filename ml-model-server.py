# from flask import Flask

# app = Flask(__name__)

# @app.route("/")
# def hello_world():
# 	return "<p>Hello, World again!</p>"

from flask import Flask

app = Flask(__name__)

@app.route('/', methods=['GET'])
def index():
    return "Hello flask server received your request"

if __name__ == "__main__":
    app.run()