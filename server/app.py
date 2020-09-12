#Import Statements
from flask import Flask
from Database import mongo
from Users import user_api
from Quiz import quiz_api
from Settings import secret_key, mongo_uri

# Flask Application
app = Flask(__name__)
app.secret_key = secret_key

# MongoDB initilization and configuration
app.config["MONGO_URI"] = mongo_uri
mongo.init_app(app)

# Registration of all blueprints in the project
app.register_blueprint(user_api, url_prefix = "/users")
app.register_blueprint(quiz_api, url_prefix = "/quiz")


if __name__ == "__main__":
    app.run(debug=True)


