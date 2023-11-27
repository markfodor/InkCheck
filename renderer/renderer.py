"""
This script essentially generates a HTML file. It then fires up a headless Chrome
instance, sized to the resolution of the eInk display and takes a screenshot.
"""

from selenium import webdriver
from selenium.webdriver.chrome.service import Service
from time import sleep
from jinja2 import Environment, FileSystemLoader
from selenium.webdriver.common.by import By
from logger.logger import logger
import pathlib
import sys
import os

class Renderer:

    def __init__(self, width, height):
        # Initialize all the file and path variables here so it is easier to track things back
        self.input_html_template = 'inkcheck_template.html'
        self.output_folder = 'output'
        self.output_image = 'inkcheck.png'
        self.output_html = 'inkcheck.html'
        self.curr_path = str(pathlib.Path(__file__).parent.absolute())
        self.project_path = os.path.abspath(os.curdir)

        logger.info(f"On platform: {sys.platform}")
        self.is_windows = sys.platform.startswith('win')
        
        self.absolute_input_html_template_path = os.path.join(self.curr_path, self.input_html_template)
        self.absolute_output_folder = os.path.join(self.project_path, self.output_folder)
        self.output_html_file_path = os.path.join(self.curr_path, self.output_html)
        self.output_image_path = os.path.join(self.absolute_output_folder, self.output_image)

        self.image_width = width
        self.image_height = height

    def set_viewport_size(self, driver):
        # Extract the current window size from the driver
        current_window_size = driver.get_window_size()

        # Extract the client window size from the html tag
        html = driver.find_element(By.TAG_NAME,'html')
        inner_width = int(html.get_attribute("clientWidth"))
        inner_height = int(html.get_attribute("clientHeight"))

        # Calculate the target width and height for the window
        target_width = self.image_width + (current_window_size["width"] - inner_width)
        target_height = self.image_height + (current_window_size["height"] - inner_height)

        driver.set_window_rect(
            width=target_width,
            height=target_height
        )

    def take_screenshot(self):
        if not os.path.exists(self.output_html_file_path):
            logger.error(f"HTML file does not exist: {self.output_html_file_path}. Probably not created properly from the template.")
            return
        
        if not os.path.exists(self.absolute_output_folder):
            os.mkdir(self.absolute_output_folder)

        opts = webdriver.ChromeOptions()
        opts.add_argument("--headless")
        opts.add_argument("--hide-scrollbars")
        opts.add_argument('--force-device-scale-factor=1')

        if not self.is_windows:
            binary_location = self.get_chrome()
            logger.info(f"Chrome driver found: {binary_location}")
            service = Service(executable_path=binary_location)
            driver = webdriver.Chrome(service=service, options=opts)
        else:
            driver = webdriver.Chrome(options=opts)
        self.set_viewport_size(driver)
        
        driver.get('file://' + self.output_html_file_path)
        sleep(1)

        success = driver.get_screenshot_as_file(self.output_image_path)
        if success:
            logger.info('Screenshot captured and saved to file.')
        else:
            logger.error('ERROR during the screen capture.')

    def render(self, timestamp, data_list):
        template_loader = FileSystemLoader(self.curr_path)
        template = Environment(loader=template_loader, autoescape=True).get_template(self.input_html_template)
        rendered_template = template.render(
            timestamp=timestamp,
            data_list=data_list
        )

        with open(self.output_html_file_path, 'w+', encoding='utf-8') as file:
            file.write(rendered_template)

        logger.info(f"Template is rendered and saved to {self.output_html_file_path}")
        self.take_screenshot()

    # find the chrome driver on Linux distros
    def get_chrome(self):
        if os.path.isfile('/usr/bin/chromedriver'):
            return '/usr/bin/chromedriver'
        elif os.path.isfile('/usr/bin/chromium-browser'):
            return '/usr/bin/chromium-browser'
        elif os.path.isfile('/usr/bin/chromium'):
            return '/usr/bin/chromium'
        elif os.path.isfile('/usr/bin/chrome'):
            return '/usr/bin/chrome'
        elif os.path.isfile('/usr/bin/google-chrome'):
            return '/usr/bin/google-chrome'
        else:
            return None
