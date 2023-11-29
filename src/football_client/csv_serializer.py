import csv
from football_client.base_serializer import BaseSerializer


class CsvSerializer(BaseSerializer):
    """
    Serialize data to CSV ot TSV
    """

    def __init__(self, data_dir, file_name, settings=None):
        """
        :param data_dir: normally ~/.football_client/data
        :param file_name: name without extension, e.g., leagues
        :param settings: dict
        """
        assert settings is None or isinstance(settings, dict), "settings must be a dict"
        assert settings is None or "headers" in settings, "headers must be specified in settings"
        assert settings is None or "columns" in settings, "columns must be specified in settings"
        assert settings is None or "delimiter" in settings, "delimiter must be specified in settings"
        super().__init__(data_dir, file_name, settings=settings)

    def write(self, data):
        """
        Serialize data to CSV or TSV
        :param data:
        :return:
        """
        headers = self.settings.get("headers", [])
        columns = self.settings.get("columns", [])
        delimiter = self.settings.get("delimiter", "\t")
        with open(self.serialized_file, "w", newline="", encoding="utf-8") as tsv_file:
            writer = csv.writer(tsv_file, delimiter=delimiter)
            # Write header
            writer.writerow(headers)
            # Write data
            for item in data:
                # Default behavior: write columns as is
                writer.writerow([item.get(col, "") for col in columns])
        print("Serialized data to TSV.")

    def read(self):
        """
        Read serialized data from CSV or TSV
        :return: list
        """
        delimiter = self.settings.get("delimiter", "\t")
        with open(self.serialized_file, "r", newline="", encoding="utf-8") as tsv_file:
            reader = csv.DictReader(tsv_file, delimiter=delimiter)
            return [row for row in reader]

    @staticmethod
    def get_extension():
        """
        Get the file extension for the serialized data format (e.g., "json", "tsv")
        """
        return "tsv"


class LeaguesCsvSerializer(CsvSerializer):
    """
    Serialize leagues data to CSV or TSV
    """

    def __init__(self, data_dir):
        """
        :param data_dir:
        """
        leagues_settings = {
            "headers": ["ID", "Name", "Type", "Country", "Seasons"],
            "columns": ["id", "name", "type", "country", "seasons"],
            "delimiter": "\t"
        }
        super().__init__(data_dir, file_name="leagues", settings=leagues_settings)

    def write(self, data):
        """
        Overload for leagues
        :param data:
        :return:
        """
        headers = self.settings.get("headers", [])
        delimiter = self.settings.get("delimiter", "\t")
        with open(self.serialized_file, "w", newline="", encoding="utf-8") as tsv_file:
            writer = csv.writer(tsv_file, delimiter=delimiter)
            # Write header
            writer.writerow(headers)
            # Write data
            for item in data:
                # Overloaded behavior: write seasons as comma-separated list
                writer.writerow([
                    item["id"],
                    item["name"],
                    item["type"],
                    item["country"], ", ".join(map(str, item["seasons"]))
                ])
        print("Serialized data to TSV.")
