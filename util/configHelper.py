import os
import json
from logger.logger import logger

def read_config(current_path):
    config_path = os.path.join(current_path, 'config.json')
    config_file = open(config_path)
    return json.load(config_file)

def validate_collectors(collectors: list[str]) -> bool:
    if not collectors:
        logger.error('Collectors setup is not valid in global.json')
        return False
    
    if any(collector == '' for collector in collectors):
        logger.error('Empty string at the collectors array in global.json')
        return False

    if len(collectors) > 2:
        logger.error('Only two collectors are allowed the global.json')
        return False

    return True