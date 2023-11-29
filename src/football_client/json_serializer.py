import os
import json
from football_client.base_serializer import BaseSerializer


class JsonSerializer(BaseSerializer):
    """
    Serialize data to JSON
    """

    def __init__(self, data_dir, file_name, settings):
        """
        :param data_dir: normally ~/.football_client/data
        :param file_name: name without extension, e.g., leagues
        :param settings: dict
        """
        super().__init__(data_dir, file_name, settings=settings)

    def write(self, data):
        """
        Serialize data to JSON
        """
        with open(self.serialized_file, "w") as json_file:
            json.dump(data, json_file, indent=4)
        print(f"Serialized data to {self.serialized_file}")

    def read(self):
        """
        Read serialized data from JSON
        :return: dict
        """
        data = {}
        if not os.path.exists(self.serialized_file):
            return data
        with open(self.serialized_file, "r") as json_file:
            data = json.load(json_file)
        return data

    @staticmethod
    def get_extension():
        """
        Get the file extension for the serialized data format (e.g., "json", "tsv")
        """
        return "json"


class LeaguesJsonSerializer(JsonSerializer):
    """
    Serialize leagues data to JSON and additional simplified files
    """

    def __init__(self, data_dir):
        super().__init__(data_dir, file_name="leagues", settings=None)

    def write(self, leagues_data):
        """
        Serialize leagues data to JSON and additional simplified files
        """
        super().write(leagues_data)  # Call the base class write method

        leagues_simplified_file = os.path.join(self.data_dir, "leagues_simplified.json")
        seasons_simplified_file = os.path.join(self.data_dir, "seasons_simplified.json")
        with open(leagues_simplified_file, "w") as leagues_json_f:
            json.dump(self._write_leagues(leagues_data), leagues_json_f, indent=4)
        with open(seasons_simplified_file, "w") as seasons_json_f:
            json.dump(self._write_seasons(leagues_data), seasons_json_f, indent=4)

        print(f"Serialized simplified leagues data to {leagues_simplified_file}")

    @staticmethod
    def _write_leagues(leagues_data):
        simplified_leagues = []
        for lg in leagues_data["response"]:
            simplified_leagues.append({
                "id": lg["league"]["id"],
                "name": lg["league"]["name"],
                "type": lg["league"]["type"],
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
                    "id": lg["league"]["id"],
                    "name": lg["league"]["name"],
                    "country": lg["country"]["name"],
                    "year": season["year"],
                    "start": season["start"],
                    "end": season["end"]
                })
        return seasons
