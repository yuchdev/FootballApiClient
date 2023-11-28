import json
import os


class LeaguesMixin:
    """
    Mixin for leagues
    """
    def __init__(self, data_dir):
        self.data_dir = data_dir
        self.leagues_simplified = os.path.join(self.data_dir, "leagues_simplified.json")
        self.seasons_simplified = os.path.join(self.data_dir, "seasons_simplified.json")

    @staticmethod
    def _write_leagues(leagues_data):
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
    def _write_seasons(leagues_data):
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

    def write(self, leagues_data):
        """
        Leave only important information
        :param leagues_data:
        :return:
        """
        print(f"Simplify from {len(leagues_data)} leagues")
        leagues_simplified = self._write_leagues(leagues_data)
        with open(self.leagues_simplified, "w") as leagues_json_f:
            json.dump(leagues_simplified, leagues_json_f, indent=4)

        seasons_simplified = self._write_seasons(leagues_data)
        with open(self.seasons_simplified, "w") as seasons_json_f:
            json.dump(seasons_simplified, seasons_json_f, indent=4)


class JsonSerializer:
    MIXINS = {
        "leagues": LeaguesMixin
    }

    def __init__(self, data_dir, file_name):
        self.data_dir = data_dir
        self.leagues_file = os.path.join(self.data_dir, file_name)

    def write(self, data):
        """
        Serialize data to JSON
        """
        with open(self.leagues_file, "w") as json_file:
            json.dump(data, json_file, indent=4)
        entity = data["get"]
        print(f"Load mixin for {entity}")
        mixin = self.MIXINS.get(entity, None)
        if mixin:
            mixin(self.data_dir).write(data)
            print("Serialized data to JSON")
        else:
            print("No specific mixin found")

    def read(self):
        """
        Read serialized data from JSON
        :return: dict
        """
        leagues_data = {}
        if not os.path.exists(self.leagues_file):
            return leagues_data
        with open(self.leagues_file, "r") as json_file:
            leagues_data = json.load(json_file)
        return leagues_data
