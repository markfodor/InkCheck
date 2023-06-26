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
from googlekeep.googlekeephelper import googleKeepHelper
from trelloparser.trellohelper import TrelloHelper


if __name__ == '__main__':
    configFile = open('config.json')
    config = json.load(configFile)

    timeZone = timezone(config['timezone'])
    timestampFormat = config['timestampFormat']
    googleKeepUsername = config['googleKeepUsername']
    googleKeepPassword = config['googleKeepPassword']
    googleKeepNoteName = config['googleKeepNoteName']
    trelloKey = config['trelloKey']
    trelloSecret = config['trelloSecret']
    trelloToken = config['trelloToken']
    trelloBoard = config['trelloBoard']
    trelloList = config['trelloList']
    imageWidth = config['imageWidth']
    imageHeight = config['imageHeight']
    rotateAngle = config['rotateAngle']
    destinationFolder = config['destinationFolder']

    logger.info('Config is set.')

    timestamp = dt.now(timeZone).strftime(timestampFormat)

    googlekeephelper = googleKeepHelper(googleKeepUsername, googleKeepPassword)
    is_google_keep_list, google_keep_items = googlekeephelper.search_note_id_by_name(googleKeepNoteName, True)

    trello_helper = TrelloHelper(trelloKey, trelloToken)
    trello_items = trello_helper.get_data(trelloBoard, trelloList)

    renderer = Renderer(imageWidth, imageHeight, rotateAngle)
    renderer.render(timestamp, googleKeepNoteName, is_google_keep_list, google_keep_items, trelloList, trello_items, destinationFolder)

    logger.info("Inkcheck is updated.")
