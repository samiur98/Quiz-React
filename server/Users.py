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
    response = dumps(all_users)
    return response

# Route for adding a user to the database
@user_api.route("/addUser", methods = ["POST"])
def add_user():
    # Checks if information provided is valid and then adds a new user to the database
    try:
        _json = request.json
        _username = _json["username"]
        _password = _json["password"]
        _email = _json["email"]

        if (len(_username) < 5) or (len(_password) < 8):
            return user_add_badfield_response()
        else:
            userExists = check_for_user(_username)
            if userExists:
                return user_add_user_exists_response(_username)
            else:
                mongo.db.users.insert({
                    "username": _username,
                    "password": generate_password_hash(_password),
                    "email": _email
                    })
                return user_add_successfull_response(_username)
    except (AttributeError, KeyError):
        return user_add_badfield_response()

# Route for validating a user based on username and password
@user_api.route("/validateUser", methods = ["POST"])
def validate_user():
    # Queries database and validates a users credentials (username and password).
    try:
        _json = request.json
        _username = _json["username"]
        _password = _json["password"]
        
        if check_with_credentials(_username, _password):
            return user_validate_success_response()
        else:
            return user_validate_failure_response()

    except (AttributeError, KeyError):
        return user_validate_badfield_response()

# Route for changing a user's email
@user_api.route("changeEmail", methods = ["PUT"])
def change_email():
    # Performs query for changing a user's email
    try:
        _json = request.json
        _username = _json["username"]
        _password = _json["password"]
        _new_email = _json["newEmail"]

        if email_change_query(_username, _password, _new_email):
            return email_change_successfull_response()
        else:
            return email_change_failure_response()

    except (AttributeError, KeyError):
        return email_change_badfield_response()

# Route for changing a user's password
@user_api.route("changePassword", methods = ["PUT"])
def change_password():
    # Performs query for changing a user's password
    try:
        _json = request.json
        _username = _json["username"]
        _old_password = _json["oldPassword"]
        _new_password = _json["newPassword"]

        if len(_new_password) < 8:
            return password_change_badfield_response()
        if password_change_query(_username, _old_password, _new_password):
            return password_change_successfull_response()
        else:
            return password_change_failure_response()
            
    except (AttributeError, KeyError):
        return password_change_badfield_response()

# Helper functions
def check_for_user(_username):
    # Method that checks if a user exists based on the provided username
    check_result = dumps(mongo.db.users.find({"username" : _username}))
    if check_result == "[]":
       return False
    else:
        return True

def user_add_badfield_response():
    # Returns the response for a POST request for adding users with invalid/insufficient 
    response = jsonify("JSON Body for addUser POST request must contain username, password and email," +
    " where the length of the username should be atleast 5 charachters long and the length of the password should be at least" +
    " 8 charachters long")
    response.status_code = 403
    return response

def user_add_user_exists_response(_username):
    # Returns the response for a POST request for adding users where a user with the provided username, already exists
    response = jsonify("User with username " + _username + " already exists")
    response.status_code = 403
    return response

def user_add_successfull_response(_username):
    # Returns the response for a POST request for adding users where the user was successfully added.
    response = jsonify("User " + _username + " successsfully added!")
    response.status_code = 201
    return response

def check_with_credentials(_username, _password):
    # Queries database and validates username and password.
    query = mongo.db.users.find_one({
        "username": _username,
    })
    if query is None:
        return False
    stored_password = query["password"]
    return check_password_hash(stored_password, _password)

def user_validate_success_response():
    # Returns the response for a POST request for validating user that was successfull.
    response = jsonify("User successfully validated")
    response.status_code = 200
    return response

def user_validate_failure_response():
    # Returns the response for a POST request for validating user that was not successfull.
    response = jsonify("Username and/or password incorrect")
    response.status_code = 404
    return response

def user_validate_badfield_response():
    # Returns the response for a POST request for validating user with insufficient/incorrect fields
    response = jsonify("Request must have username and password fields in the request body")
    response.status_code = 403
    return response

def email_change_query(_username, _password, _email):
    # Query for changing a user's email
    find_query = {"username": _username}
    update_query =  {"$set": {"email": _email}}
    if check_with_credentials(_username, _password):
        mongo.db.users.update_one(find_query, update_query)
        return True
    else:
        return False

def email_change_successfull_response():
    # Returns the response for a successfull PUT request for changing a user's email address
    response = jsonify("Email successfully updated")
    response.status_code = 200
    return response

def email_change_badfield_response():
    # Returns the response for a PUT request for changing a user's email with insufficient/bad fields
    response = jsonify("Request must have username, password, and newEmail in the request body")
    response.status_code = 403
    return response

def email_change_failure_response():
    # Returns the response for a PUT request for changing a user's email that failed
    response = jsonify("Email address could not be changed")
    response.status_code = 400
    return response

def password_change_query(_username, _old_password, _new_password):
    # Query for updating a user's password
    if(check_with_credentials(_username, _old_password)):
        find_query = {"username": _username}
        update_query = {"$set": {"password": generate_password_hash(_new_password)}}
        mongo.db.users.update_one(find_query, update_query)
        return True
    else:
        return False

def password_change_successfull_response():
    # Returns the response for a successfull PUT request for changing a user's password
    response = jsonify("Password successfully updated")
    response.status_code = 200
    return response

def password_change_failure_response():
    # Returns the response for an unsuccesfull PUT request for changing a user's password
    response = jsonify("Password could not be changed")
    response.status_code = 400
    return response

def password_change_badfield_response():
    # Returns the response for a PUT reqeust for changing a user's password with insufficient/bad fields
    response = jsonify("Request must have username, oldPassword, newPassword fields where newPassword and oldPassword must be atleast 8 charachters long")
    response.status_code = 403
    return response