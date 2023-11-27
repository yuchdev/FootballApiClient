import csv
import http.client
import json
import os.path
from api_key import API_KEY

headers = {
    'x-rapidapi-host': "v3.football.api-sports.io",
    'x-rapidapi-key': API_KEY
}



class SerializeTsv:
    def __init__(self, data_dir):
        self.data_dir = data_dir

    def serialize(self, data):
        file_path = os.path.join(self.data_dir, "leagues_simplified.tsv")
        with open(file_path, "w", newline="", encoding="utf-8") as tsv_file:
            writer = csv.writer(tsv_file, delimiter="\t")
            # Write header
            writer.writerow(["id", "name", "type," "country", "seasons"])
            # Write data
            for item in data:
                writer.writerow([item["id"], item["name"], item["country"], ", ".join(map(str, item["seasons"]))])
        print("Serialized data to TSV.")


class WorldLeagues:
    def __init__(self):
        self.leagues = []
        self.data_dir = os.path.join(os.path.dirname(__file__), "data")
        self.leagues_file = os.path.join(self.data_dir, "leagues.json")
        self.leagues_simplified = os.path.join(self.data_dir, "leagues_simplified.json")
        self.seasons_simplified = os.path.join(self.data_dir, "seasons_simplified.json")

    def _get_league(self, league_id=None, league_name=None):
        """
        Check if the league is already in the cache
        If not in cache, check the JSON file
        :param league_id: e.g. 39
        :param league_name: e.g. Bundesliga
        :return: dict
        """
        if self.leagues:
            print("Using cached leagues data")
            for lg in self.leagues:
                if (league_id and lg.id == league_id) or (league_name and lg.name == league_name):
                    return lg

        if os.path.isfile(self.leagues_file):
            print(f"Using leagues data from file: {self.leagues_file}")
            with open(self.leagues_file, "r") as leagues_json_f:
                leagues_data = json.load(leagues_json_f)
            self._simplify(leagues_data)
            for league_data in leagues_data["response"]:
                if (league_id and league_data["league"]["id"] == league_id) or (league_name and league_data["league"]["name"] == league_name):
                    return league_data
            return {}
        else:
            print(f"Fetching leagues data from URL {headers['x-rapidapi-host']}...")
            return self._request()

    @staticmethod
    def _simplify_leagues(leagues_data):
        """
        Leave only important information
        """
        simplified_leagues = []
        for lg in leagues_data["response"]:
            simplified_leagues.append({
                "id": lg["league"]["id"],
                "name": lg["league"]["name"],
                "country": lg["country"]["name"],
                "seasons": [season["year"] for season in lg["seasons"]],
            })
        return simplified_leagues

    @staticmethod
    def _simplify_seasons(leagues_data):
        seasons = []
        for lg in leagues_data["response"]:
            for season in lg["seasons"]:
                seasons.append({
                    "league_id": lg["league"]["id"],
                    "league_name": lg["league"]["name"],
                    "country": lg["country"]["name"],
                    "year": season["year"],
                    "start": season["start"],
                    "end": season["end"]
                })
        return seasons

    def _simplify(self, leagues_data):
        """
        Leave only important information
        :param leagues_data:
        :return:
        """
        print(f"Simplify from {len(leagues_data)} leagues")
        leagues_simplified = self._simplify_leagues(leagues_data)
        with open(self.leagues_simplified, "w") as leagues_json_f:
            json.dump(leagues_simplified, leagues_json_f, indent=4)

        seasons_simplified = self._simplify_seasons(leagues_data)
        with open(self.seasons_simplified, "w") as seasons_json_f:
            json.dump(seasons_simplified, seasons_json_f, indent=4)

    def _request(self):
        conn = http.client.HTTPSConnection("v3.football.api-sports.io")
        endpoint = "/leagues"
        conn.request("GET", endpoint, headers=headers)
        result = conn.getresponse()
        result_data = result.read()
        leagues_data = json.loads(result_data)

        # Check for API errors
        if "errors" in leagues_data:
            raise Exception(f"API Error: {leagues_data['errors']}")

        # Cache the data
        with open(self.leagues_file, "w") as leagues_json_f:
            json.dump(leagues_data, leagues_json_f, indent=4)

        # Simplify the data for easier use in data analysis
        self._simplify(leagues_data)

        return leagues_data

    def by_id(self, league_id):
        return self._get_league(league_id=league_id)

    def by_name(self, league_name):
        return self._get_league(league_name=league_name)

    def all(self):
        leagues_data = self._get_league()
        return leagues_data["response"]

    def serialize(self, serializer="json"):
        leagues_data = self._get_league()
        serializer_class = self.serializer_classes.get(serializer)

        if serializer_class:
            simplified_data = self._simplify_leagues(leagues_data)
            serializer_class.serialize(simplified_data)
        else:
            print("Invalid serializer selected.")

class League:
    def __init__(self, league_data):
        self.id = league_data["league"]["id"]
        self.type = league_data["league"]["type"]
        self.name = league_data["league"]["name"]
        self.country = league_data["country"]["name"]
        self.seasons = [season["year"] for season in league_data["seasons"]]
        self.players = []


# Usage example
world = WorldLeagues()
league_by_id = world.by_id(4)

if league_by_id:
    print(f"League found by ID: {league_by_id['league']['name']}")
