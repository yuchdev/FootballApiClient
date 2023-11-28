import http.client
import json
import os.path
from api_key import API_KEY
from json_serializer import JsonSerializer
from csv_serializer import CsvSerializer

headers = {
    'x-rapidapi-host': "v3.football.api-sports.io",
    'x-rapidapi-key': API_KEY
}


SERIALIZERS = {
    "json": JsonSerializer,
    "csv": CsvSerializer
}


class WorldLeagues:
    def __init__(self, serializer: str):
        self.leagues = {}
        self.data_dir = os.path.join(os.path.dirname(__file__), "data")
        self.serializer = SERIALIZERS.get(serializer, JsonSerializer)(self.data_dir)

    def get_league(self, league_id=None, league_name=None):
        """
        Check if the league is already in the cache
        If not in cache, check the JSON file
        :param league_id: e.g. 39
        :param league_name: e.g. Bundesliga
        :return: dict
        """
        print(f"Getting league information for {league_id or league_name}")
        if not self.leagues:
            print("No cached leagues data. Trying to read from serialized data...")
            self.leagues = self.serializer.read()

            if not self.leagues:
                print("Serialized data is empty or not found. Fetching from API...")
                self.leagues = self._request()

        for lg in self.leagues['response']:
            if (league_id and lg["league"]["id"] == league_id) or (league_name and lg["league"]["name"] == league_name):
                return lg
        return {}

    def _request(self):
        conn = http.client.HTTPSConnection("v3.football.api-sports.io")
        endpoint = "/leagues"
        conn.request("GET", endpoint, headers=headers)
        result = conn.getresponse()
        result_data = result.read()
        leagues_data = json.loads(result_data)

        # Check for API errors
        if "errors" in leagues_data and len(leagues_data["errors"]):
            raise Exception(f"API Error: {leagues_data['errors']}")

        self.serializer.write(data=leagues_data)
        return leagues_data

    def by_id(self, league_id):
        assert isinstance(league_id, int), "League ID must be an integer"
        return self.get_league(league_id=league_id)

    def by_name(self, league_name):
        assert isinstance(league_name, str), "League name must be a string"
        return self.get_league(league_name=league_name)

    def all(self):
        leagues_data = self.get_league()
        return leagues_data["response"]


class League:
    def __init__(self, league_data):
        self.id = league_data["league"]["id"]
        self.type = league_data["league"]["type"]
        self.name = league_data["league"]["name"]
        self.country = league_data["country"]["name"]
        self.seasons = [season["year"] for season in league_data["seasons"]]
        self.players = []
