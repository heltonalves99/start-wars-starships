from flask import Flask
from flask_restplus import Api
from api.config import Config

from api.starships import blueprint as starships


def create_app():
    app = Flask(__name__, instance_relative_config=True)
    app.config.from_object(Config)

    app.register_blueprint(starships, url_prefix=app.config["API_PREFIX"])
    return app
