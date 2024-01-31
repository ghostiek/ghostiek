from flask import Flask
import db_utils as db


app = Flask(__name__)


@app.route("/getData")
def hello():
    creds = db.get_creds()
    result = db.read_data(creds)
    return result


if __name__ == "__main__":
    app.run(ssl_context='adhoc')
