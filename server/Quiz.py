#Import Statements
from flask import Blueprint
from bson.json_util import dumps
from bson.objectid import ObjectId
from flask import jsonify, request
from werkzeug.security import generate_password_hash, check_password_hash
from Database import mongo

quiz_api = Blueprint("quiz_api", __name__)

# Route for getting all quizzes in the database
@quiz_api.route("/getAll", methods = ["GET"])
def get_quizzes():
    # Queries for all quizzes stored in the database
    all_quizzes = mongo.db.quiz.find()
    response = dumps(all_quizzes)
    return response

# Route for getting two random quizzes in the database
@quiz_api.route("/getRandom", methods = ["GET"])
def get_random_quizzes():
    # Queries for two random quizzes from the database.
    random_quizzes = mongo.db.quiz.aggregate([{"$sample": {"size": 2}}])
    response = dumps(random_quizzes)
    return response

# Route for adding quiz to the database
@quiz_api.route("addQuiz", methods = ["POST"])
def add_quiz():
    # Makes query that adds a quiz to the database.
    try:
        _json = request.json
        _title = _json["title"]
        _description = _json["description"]
        _username = _json["username"]
        _questions = _json["questions"]

        mongo.db.quiz.insert({
            "title": _title,
            "description": _description,
            "username": _username,
            "questions": _questions
        })

        return add_quiz_successfull_response()

    except (AttributeError, KeyError):
        return add_quiz_badfield_response()

# Route for deleting a quiz based on the quizzes ObjectID
@quiz_api.route("deleteQuiz/<quizID>", methods = ["DELETE"])
def deleteQuiz(quizID):
    # Makes query that deletes a quiz from the database.
    mongo.db.quiz.delete_one({"_id": ObjectId(quizID)})
    response = jsonify("Quiz deleted successfully")
    response.status_code = 200
    return response


# Helper functions

def add_quiz_successfull_response():
    # Returns the response for a successfull POST request for adding a quiz
    response = jsonify("Quiz Successfully added")
    response.status_code = 201
    return response

def add_quiz_badfield_response():
    # Returns the response for a POST request for adding a quiz with insufficient/bad fields
    response = jsonify("Fields provided in request body are insufficient/bad")
    response.status_code = 403
    return response
