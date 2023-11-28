import http.client
import json
from football_client.settings import API_KEY, DATA_DIR
from football_client.json_serializer import JsonSerializer
from football_client.csv_serializer import CsvSerializer

API_HOST = "v3.football.api-sports.io"
HEADERS = {
    'x-rapidapi-host': API_HOST,
    'x-rapidapi-key': API_KEY
}
SERIALIZERS = {
    "json": JsonSerializer,
    "csv": CsvSerializer
}


class World:
    """
    Get information about leagues and countries
    """

    def __init__(self, serializer: str):
        self.leagues = {}
        self.countries = {}
        self.data_dir = DATA_DIR
        # Use for caching in data directory
        self.caching = {
            "leagues": self._create_serializer(serializer="json", entity="leagues"),
            "countries": self._create_serializer(serializer="json", entity="countries")
        }
        # Use for serializing to user-specified format
        self.serializers = {
            "leagues": self._create_serializer(serializer=serializer, entity="leagues"),
            "countries": self._create_serializer(serializer=serializer, entity="countries")
        }

    def _create_serializer(self, serializer: str, entity: str):
        """
        Create serializer of the given type for the given entity
        """
        assert serializer in SERIALIZERS, f"Serializer {serializer} is not supported"
        return SERIALIZERS[serializer](self.data_dir, entity)

    def _request(self, entity):
        """
        Request data from API
        :param entity: e.g. leagues
        :return: dict
        """
        conn = http.client.HTTPSConnection(API_HOST)
        endpoint = f"/{entity}"
        conn.request("GET", endpoint, headers=HEADERS)
        result = conn.getresponse()
        result_data = json.loads(result.read())

        # Check for API errors
        if "errors" in result_data and len(result_data["errors"]):
            raise Exception(f"API Error: {result_data['errors']}")

        # Cache the data
        # TODO: split caching and serialization into separate abstract layers
        self.caching[entity].write(data=result_data)
        self.serializers[entity].write(data=result_data)

        return result_data

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
            self.leagues = self.caching['leagues'].read()

        if not self.leagues:
            print("Serialized data is empty or not found. Fetching from API...")
            self.leagues = self._request("leagues")

        for lg in self.leagues['response']:
            if (league_id and lg["league"]["id"] == league_id) or (league_name and lg["league"]["name"] == league_name):
                return lg
        return {}

    def get_country(self, country_name=None, country_code=None):
        """
        Get country
        :return: dict
        """
        print(f"Getting country information for {country_name or country_code}")
        if not self.countries:
            print("No cached countries data. Trying to read from serialized data...")
            self.countries = self.caching['countries'].read()

        if not self.countries:
            print("Serialized data is empty or not found. Fetching from API...")
            self.countries = self._request("countries")

        for country in self.countries['response']:
            if (country_name and country["name"] == country_name) or (country_code and country["code"] == country_code):
                return country
        return {}

    def all_leagues(self):
        self.get_league()
        return self.leagues["response"]

    def all_countries(self):
        self.get_country()
        return self.countries["response"]


class League:
    def __init__(self, league_data):
        self.id = league_data["league"]["id"]
        self.type = league_data["league"]["type"]
        self.name = league_data["league"]["name"]
        self.country = league_data["country"]["name"]
        self.seasons = [season["year"] for season in league_data["seasons"]]
        self.players = []
