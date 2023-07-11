import os
import json

def read_config(current_path):
    config_path = os.path.join(current_path, 'config.json')
    config_file = open(config_path)
    return json.load(config_file)