#Import Statements
from flask import Flask, Blueprint
from flask_pymongo import PyMongo
from bson.json_util import dumps
from bson.objectid import ObjectId
from flask import jsonify, request
from werkzeug.security import generate_password_hash, check_password_hash
from Database import mongo

user_api = Blueprint("user_api", __name__)

# Route for getting all users in the database
@user_api.route("/getAll", methods=["GET"])
def get_users():
    # Queries for all users in the database and returns a response object with the result of the query.
    all_users = mongo.db.users.find()
    resp = dumps(all_users)
    return resp

# Route for adding a user to the database
@user_api.route("/addUser", methods=["POST"])
def add_user():
    # Checks if information provided is valid and then adds a new user to the database