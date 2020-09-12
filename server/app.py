#Import Statements
from flask import Flask
from Database import mongo
from Users import user_api
from Quiz import quiz_api

# Flask Application
app = Flask(__name__)
app.secret_key = "tempSecretKey"

# MongoDB initilization and configuration
app.config["MONGO_URI"] = "mongodb://localhost:27017/quiz-react"
mongo.init_app(app)

# Registration of all blueprints in the project
app.register_blueprint(user_api, url_prefix = "/users")
app.register_blueprint(quiz_api, url_prefix = "/quiz")


if __name__ == "__main__":
    app.run(debug=True)


