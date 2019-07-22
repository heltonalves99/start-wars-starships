import os


class Config:
    SECRET_KEY = os.environ.get("SECRET_KEY", "star-wars-dev")
    API_PREFIX = "/api"
