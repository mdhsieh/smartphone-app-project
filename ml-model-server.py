# from flask import Flask

# app = Flask(__name__)

# @app.route("/")
# def hello_world():
# 	return "<p>Hello, World again!</p>"

from flask import Flask

app = Flask(__name__)

@app.route('/')
def index():
    return "Hello this is flask server welcome message"

if __name__ == "__main__":
    app.run()