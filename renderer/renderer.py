"""
This script essentially generates a HTML file. It then fires up a headless Chrome
instance, sized to the resolution of the eInk display and takes a screenshot.
"""

from jinja2 import Environment, FileSystemLoader
from selenium.webdriver.common.by import By
from logger.logger import logger
import pathlib
import os
from playwright.sync_api import sync_playwright


class Renderer:

    def __init__(self, width, height):
        # Initialize all the file and path variables here so it is easier to track things back
        self.input_html_template = 'inkcheck_template.html'
        self.output_folder = 'output'
        self.output_image = 'inkcheck.png'
        self.output_html = 'inkcheck.html'
        self.curr_path = str(pathlib.Path(__file__).parent.absolute())
        self.project_path = os.path.abspath(os.curdir)

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
        html = driver.find_element(By.TAG_NAME, 'html')
        inner_width = int(html.get_attribute("clientWidth"))
        inner_height = int(html.get_attribute("clientHeight"))

        # Calculate the target width and height for the window
        target_width = self.image_width + (current_window_size["width"] - inner_width)
        target_height = self.image_height + (current_window_size["height"] - inner_height)

        driver.set_window_rect(
            width=target_width,
            height=target_height
        )

    def _take_screenshot(self):
        if not os.path.exists(self.output_html_file_path):
            logger.error(
                f"HTML file does not exist: {self.output_html_file_path}. Probably not created properly from the template.")
            return

        if not os.path.exists(self.absolute_output_folder):
            os.mkdir(self.absolute_output_folder)

        with sync_playwright() as playwright:
            webkit = playwright.webkit
            browser = webkit.launch()
            context = browser.new_context()
            page = context.new_page()
            page.goto(f"file://{self.output_html_file_path}")
            page.screenshot(path=self.output_image_path)
            browser.close()

    def render(self, timestamp, data_list, destination_folder):
        template_loader = FileSystemLoader(self.curr_path)
        template = Environment(loader=template_loader, autoescape=True).get_template(self.input_html_template)
        rendered_template = template.render(
            timestamp=timestamp,
            data_list=data_list
        )

        with open(self.output_html_file_path, 'w+', encoding='utf-8') as file:
            file.write(rendered_template)

        logger.info(f"Template is rendered and saved to {self.output_html_file_path}")

        if not destination_folder or not os.path.isdir(destination_folder):
            logger.error('Destination folder is not configured properly.')
            return

        if not os.path.exists(destination_folder):
            os.makedirs(destination_folder)
            logger.info(f"Destination folder created: {destination_folder}")

        self._take_screenshot()
