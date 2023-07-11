"""
This project is designed for the Inkplate 10 display. However, since the server code is only generating an image, it can
be easily adapted to other display sizes and resolution by adjusting the config settings, HTML template and
CSS stylesheet.
"""

import json
from datetime import datetime as dt
from pytz import timezone
from logger.logger import logger
from renderer.renderer import Renderer
from collectors.googlekeep.googleKeepCollector import GoogleKeepHelper
from collectors.trello.trelloCollector import TrelloCollector


if __name__ == '__main__':
    configFile = open('global.json')
    config = json.load(configFile)

    timeZone = timezone(config['timezone'])
    timestampFormat = config['timestampFormat']
    imageWidth = config['imageWidth']
    imageHeight = config['imageHeight']
    rotateAngle = config['rotateAngle']
    destinationFolder = config['destinationFolder']

    logger.info('Global config is set.')

    timestamp = dt.now(timeZone).strftime(timestampFormat)
    google_keep_data = GoogleKeepHelper().search_node_id_by_name(True)
    trello_data = TrelloCollector().get_data()

    renderer = Renderer(imageWidth, imageHeight, rotateAngle)
    renderer.render(timestamp, google_keep_data, trello_data, destinationFolder)

    logger.info("Inkcheck image is updated.")
