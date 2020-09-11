#Import Statements
from flask import Flask
from flask_pymongo import PyMongo
from bson.json_util import dumps
from bson.objectid import ObjectId
from flask import jsonify, request
from werkzeug.security import generate_password_hash, check_password_hash
from Database import mongo
from Users import user_api

# Flask Application
app = Flask(__name__)
app.secret_key = "tempSecretKey"

# MongoDB initilization and configuration
app.config["MONGO_URI"] = "mongodb://localhost:27017/quiz-react"
mongo.init_app(app)

# Registration of all blueprints in the project
app.register_blueprint(user_api, url_prefix = "/users")


if __name__ == "__main__":
    app.run(debug=True)


