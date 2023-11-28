import os
import json


def get_api_key():
    api_key = os.environ.get("FOOTBALL_API_KEY")
    if api_key:
        return api_key
    elif os.path.isfile(os.path.join(os.path.expanduser("~"), ".football_api", ".api_key.json")):
        with open(os.path.join(os.path.expanduser("~"), ".football_api", ".api_key.json")) as json_file:
            data = json.load(json_file)
            return data["FOOTBALL_API_KEY"]
    else:
        raise Exception("No API key found. Please set the environment variable FOOTBALL_API_KEY or create a file "
                        "in ~/.football_api/.api_key.json with the API key.")


def get_data_dir():
    """
    Get the data directory
    Create if it doesn't exist
    """
    data_dir = os.environ.get("FOOTBALL_DATA_DIR")
    if not data_dir:
        data_dir = os.path.join(os.path.expanduser("~"), ".football_api", "data")
    if not os.path.isdir(data_dir):
        os.makedirs(data_dir)
    return data_dir

API_KEY = get_api_key()
DATA_DIR = get_data_dir()

