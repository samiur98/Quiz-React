#Import Statements
from flask import Flask
from flask_pymongo import PyMongo
from bson.json_util import dumps
from bson.objectid import ObjectId
from flask import jsonify, request
from werkzeug.security import generate_password_hash, check_password_hash

# Flask Application
app = Flask(__name__)
app.secret_key = "tempSecretKey"

if __name__ == "__main__":
    app.run(debug=True)


