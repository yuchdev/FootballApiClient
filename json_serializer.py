import json


class JsonSerializer:
    def __init__(self, data_dir):
        self.data_dir = data_dir

    def serialize(self, data):
        file_path = os.path.join(self.data_dir, "leagues_simplified.json")
        with open(file_path, "w") as json_file:
            json.dump(data, json_file, indent=4)
        print("Serialized data to JSON.")