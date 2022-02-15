from flask import Flask

app = Flask(__name__)


# By default Flask uses get, same as
@app.route('/', methods=['GET'])
# @app.route('/')
def index():
    return "Hello, this is flask server welcome message again."

if __name__ == "__main__":
    app.run()