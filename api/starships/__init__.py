from flask import Blueprint
from flask_restplus import Api

from .starships import ns

blueprint = Blueprint("api", __name__)

api = Api(
    blueprint,
    title="Star Wars",
    description="Starships from the Star Wars movies",
)

api.add_namespace(ns, path="/starships")
