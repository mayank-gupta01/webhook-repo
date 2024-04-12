from flask import Flask
from flask_cors import CORS
from app.webhook.routes import webhook
# from app.extensions import initialize_mongo

# Creating our flask app
def create_app():

    app = Flask(__name__)
    cors = CORS(app)
    # initialize_mongo(app)
    # registering all the blueprints
    app.register_blueprint(webhook)
    return app
