"""
This project is designed for the Inkplate 10 display. However, since the server code is only generating an image, it can
be easily adapted to other display sizes and resolution by adjusting the config settings, HTML template and
CSS stylesheet.
"""

import pytz
import pathlib
from datetime import datetime as dt
from flask import Flask, jsonify, send_file
from logger.logger import logger
from renderer.renderer import Renderer
from model.columnData import ColumnData
from collectors.abstractBaseCollector import AbstractBaseCollector
from util.configHelper import validate_collectors
from config.appReader import read_appconfig

# Import the collector here so it can be in globals
from collectors.googlekeep.googleKeepCollector import GoogleKeepCollector
from collectors.trello.trelloCollector import TrelloCollector

app = Flask(__name__)
app_config = None

@app.route('/image', methods=['GET'])
def get_image():
    logger.info('Getting image...')

    current_path: str = str(pathlib.Path(__file__).parent.absolute())
    return send_file(f"{current_path}/output/inkcheck.png", mimetype='image/png')

@app.route('/', methods=['GET'])
def read_root():
   return jsonify({'message': 'Server is running.'})

@app.route('/logs', methods=['GET'])
def read_logs():
   with open('./app.log', "r") as log_file:
         return log_file.read()
    
@app.route('/generate', methods=['GET'])
def generate():
   if(not app_config):
       message = 'AppConfig is not set properly.'
       logger.warn(message)
       return jsonify({'message': message})

   logger.info('Generating image...')

   valid = validate_collectors(app_config.collectors)
   if not valid:
      error_message = 'Invalid config.'
      logger.error(error_message)
      return jsonify({'message': error_message})

   timestamp = dt.now(pytz.timezone(app_config.timezone)).strftime(app_config.timestampFormat)
   data_list: list[ColumnData] = []
   for collector_name in app_config.collectors:
      clazz = globals()[collector_name]
      collector: AbstractBaseCollector = clazz()
      data_list.append(collector.get_data())

   renderer = Renderer(app_config.imageWidth, app_config.imageHeight)
   renderer.render(timestamp, data_list, app_config.destinationFolder)

   response = 'Inkcheck image is updated.'
   logger.info(response)
   return jsonify({'message': response})

if __name__ == '__main__':
   app_config = read_appconfig('./global.json')
   logger.info('Global config is set.')
   
   app.run()