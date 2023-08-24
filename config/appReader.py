import os
import json
from config.model.appConfig import AppConfig

def read_appconfig(path):
    config_path = os.path.abspath(path)

    with open(config_path, "r") as json_file:
        json_data = json_file.read()
        json_config  = json.loads(json_data)
        return AppConfig(**json_config)