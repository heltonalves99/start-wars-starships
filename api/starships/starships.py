import requests

from flask import request, url_for
from flask_restplus import Namespace, Resource

SWAPI_URL = "https://swapi.co/api/"

ns = Namespace(
    "starships",
    description="This should retrieve a list of all starships from the Star Wars movies.",
)


@ns.route("/")
class StarshipList(Resource):

    def get(self):
        '''List all starships sorted by hyperdrive rating.'''

        try:
            page = int(request.args.get('page', 1))
            return self.get_starships(page)
        except requests.exceptions.HTTPError as error:
            if error.response.status_code == 404:
                return {
                    "error": "Page not found"
                }, 404
            return {
                "error": "External resource temporally unvailable."
            }, 503

    def get_starships(self, page=1):
        url = f"{SWAPI_URL}starships/?page={page}"

        data = {
            "starships": [],
            "starships_unknown_hyperdrive": [],
            "next": None,
            "prev": None,
        }

        resp = requests.get(url)
        resp.raise_for_status()

        obj_list = resp.json()
        starships, starships_unknown_hyperdrive = self.parse_data(obj_list["results"])
        data["starships"] = starships
        data["starships_unknown_hyperdrive"] = starships_unknown_hyperdrive

        data["starships"].sort(key=lambda key: key["hyperdrive"])

        if obj_list["next"]:
            data["next"] = self.get_url_page(page + 1)

        if obj_list["previous"]:
            data["prev"] = self.get_url_page(page - 1)
        return data

    def parse_data(self, obj_list):
        starships_unknown_hyperdrive = []
        starships = []

        for item in obj_list:
            if item["hyperdrive_rating"] == "unknown":
                starships_unknown_hyperdrive.append(
                    {"name": item["name"]}
                )
            else:
                starships.append(
                    {
                        "name": item["name"],
                        "hyperdrive": item["hyperdrive_rating"],
                    }
                )

        return starships, starships_unknown_hyperdrive

    def get_url_page(self, page):
        return f"{self.api.base_url}starships/?page={page}"
