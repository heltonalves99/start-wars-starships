import requests

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
            return self.get_starships()
        except requests.exceptions.RequestException as error:
            return {}

    def get_starships(self):
        url = f"{SWAPI_URL}starships/"

        data = {
            "starships": [],
            "starships_unknown_hyperdrive": [],
        }

        while True:
            resp = requests.get(url)
            obj_list = resp.json()
            starships, starships_unknown_hyperdrive = self.parse_data(obj_list["results"])
            data["starships"] += starships
            data["starships_unknown_hyperdrive"] += starships_unknown_hyperdrive

            if not obj_list["next"]:
                break

            url = obj_list["next"]

        data["starships"].sort(key=lambda key: key["hyperdrive"])
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
