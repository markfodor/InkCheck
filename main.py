"""
This project is designed for the Inkplate 10 display. However, since the server code is only generating an image, it can
be easily adapted to other display sizes and resolution by adjusting the config settings, HTML template and
CSS stylesheet.
"""

import json
import pathlib
from pytz import timezone
from datetime import datetime as dt
from flask import Flask, jsonify, send_file
from logger.logger import logger
from renderer.renderer import Renderer
from model.columnData import ColumnData
from collectors.abstractBaseCollector import AbstractBaseCollector
from util.configHelper import validate_collectors

# Import the collector here so it can be in globals
from collectors.googlekeep.googleKeepCollector import GoogleKeepCollector
from collectors.trello.trelloCollector import TrelloCollector

app = Flask(__name__)

@app.route('/image', methods=['GET'])
def get_image():
    logger.info('Getting image...')

    current_path: str = str(pathlib.Path(__file__).parent.absolute())
    return send_file(f"{current_path}/output/inkcheck.png", mimetype='image/png')
    
@app.route('/generate', methods=['GET'])
def generate():
   logger.info('Generating image...')

   config_file = open('global.json')
   config = json.load(config_file)

   time_zone: str = timezone(config['timezone'])
   timestamp_format: str = config['timestampFormat']
   image_width: int = config['imageWidth']
   image_height: int = config['imageHeight']
   collectors: list[str] = config['collectors']
   destination_folder: str = config['destinationFolder']

   valid = validate_collectors(collectors)
   if not valid:
      error_message = 'Invalid config.'
      logger.error(error_message)
      return jsonify({'message': error_message})

   logger.info('Global config is set.')

   timestamp = dt.now(time_zone).strftime(timestamp_format)
   data_list: list[ColumnData] = []
   for collector_name in collectors:
      clazz = globals()[collector_name]
      collector: AbstractBaseCollector = clazz()
      data_list.append(collector.get_data())

   renderer = Renderer(image_width, image_height)
   renderer.render(timestamp, data_list, destination_folder)

   response = 'Inkcheck image is updated.'
   logger.info(response)
   return jsonify({'message': response})

if __name__ == '__main__':
   app.run()