from flask import Flask
import db_utils as db


app = Flask(__name__)

@app.route("/")
def hey():
    return "Hello World"

@app.route("/getData")
def getData():
    creds = db.get_creds()
    result = db.read_data(creds)
    return result


if __name__ == "__main__":
    app.run(host="localhost")
