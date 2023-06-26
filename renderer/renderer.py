"""
This script essentially generates a HTML file. It then fires up a headless Chrome
instance, sized to the resolution of the eInk display and takes a screenshot.
"""

from selenium import webdriver
from selenium.webdriver.chrome.options import Options
from time import sleep
from jinja2 import Environment, FileSystemLoader
from selenium.webdriver.common.by import By
from logger.logger import logger
import pathlib
import shutil
import os

class Renderer:

    def __init__(self, width, height, angle):
        # init all the file and path variables here so it is easier to track things back
        self.inputHtmlTemplate = 'inkcheck_template.html'
        self.outputfolder = 'output'
        self.outputImage = 'inkcheck.png'
        self.outputHtml = 'inkcheck.html'
        self.currPath = str(pathlib.Path(__file__).parent.absolute())
        self.projectPath = os.path.abspath(os.curdir)
        
        self.absoluteInputHtmlTemplatePath = os.path.join(self.currPath, self.inputHtmlTemplate)
        self.absoluteOutputFolder = os.path.join(self.projectPath, self.outputfolder)
        self.outputHtmlFilePath = os.path.join(self.currPath, self.outputHtml)
        self.outputImagePath = os.path.join(self.absoluteOutputFolder, self.outputImage)

        self.imageWidth = width
        self.imageHeight = height
        self.rotateAngle = angle

    def set_viewport_size(self, driver):

        # Extract the current window size from the driver
        current_window_size = driver.get_window_size()

        # Extract the client window size from the html tag
        html = driver.find_element(By.TAG_NAME,'html')
        inner_width = int(html.get_attribute("clientWidth"))
        inner_height = int(html.get_attribute("clientHeight"))

        # "Internal width you want to set+Set "outer frame width" to window size
        target_width = self.imageWidth + (current_window_size["width"] - inner_width)
        target_height = self.imageHeight + (current_window_size["height"] - inner_height)

        driver.set_window_rect(
            width = target_width,
            height = target_height
        )

    def take_screenshot(self):
        if not os.path.exists(self.outputHtmlFilePath):
            logger.error(f"HTML file does not exist: {self.outputHtmlFilePath}. Probably not created properly from the template.")
            return
        
        if not os.path.exists(self.absoluteOutputFolder):
            os.mkdir(self.absoluteOutputFolder)

        opts = Options()
        opts.add_argument("--headless")
        opts.add_argument("--hide-scrollbars")
        opts.add_argument('--force-device-scale-factor=1')
        driver = webdriver.Chrome(options=opts)
        self.set_viewport_size(driver)
        
        driver.get('file://' + self.outputHtmlFilePath)
        sleep(1)

        succuess = driver.get_screenshot_as_file(self.outputImagePath)
        if succuess:
            logger.info('Screenshot captured and saved to file.')
        else:
            logger.error('ERROR during the screen capture.')

# timestamp, googleKeepNoteName, google_keep_items, trelloList, trello_items, destinationFolder
    def render(self, timestamp, googleKeepNoteName, is_google_keep_list, google_keep_items, trello_list_name, trello_items, destinationFolder):
        templateLodaer = FileSystemLoader(self.currPath)
        template = Environment(loader = templateLodaer).get_template(self.inputHtmlTemplate)
        rendered_template = template.render(
            timestamp = timestamp,
            googleKeepNoteName = googleKeepNoteName,
            is_google_keep_list = is_google_keep_list,
            google_keep_note_items = google_keep_items,
            trello_list_name = trello_list_name,
            trello_items = trello_items
        )

        with open(self.outputHtmlFilePath, 'w+', encoding = 'utf-8') as file:
            file.write(rendered_template)

        logger.info(f"Template is rendered and saved to {self.outputHtmlFilePath}")
        self.take_screenshot()

        self.copy_to_destionation_folder(destinationFolder)
    
    def copy_to_destionation_folder(self, destinationFolder):
        if not os.path.exists(destinationFolder):
            os.mkdir(destinationFolder)
            logger.info(f"Destination folder created: {destinationFolder}")
        
        shutil.copy(self.outputImagePath, destinationFolder)
        logger.info(f"Image copied to destination folder: {destinationFolder}")

        

