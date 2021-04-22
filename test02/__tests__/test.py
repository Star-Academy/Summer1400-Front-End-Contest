import os
import pprint
import re
import subprocess
import sys
import unittest
from unittest.util import three_way_cmp

from selenium import webdriver
from selenium.webdriver.common.desired_capabilities import DesiredCapabilities
from selenium.webdriver.common.by import By
from selenium.webdriver.support.ui import WebDriverWait
from selenium.webdriver.support import expected_conditions as EC
from selenium.webdriver.common.action_chains import ActionChains

import time

DEBUG = 'PRODUCTION' not in os.environ

SRC_PATH = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))
PORT = '9988'


class SimpleTest(unittest.TestCase):
    @classmethod
    def setUpClass(cls):
        print('DEBUG = {}'.format(DEBUG), file=sys.stderr)
        cls.server = subprocess.Popen(
            ['python3', '-m', 'http.server', PORT], cwd=SRC_PATH, stderr=subprocess.DEVNULL)

        desired_capabilities = dict(
            {'loggingPrefs': {'browser': 'ALL'}}, **DesiredCapabilities.CHROME)

        if DEBUG:
            cls.driver = webdriver.Chrome(
                executable_path="/usr/lib/chromium/chromedriver", desired_capabilities=desired_capabilities)
        else:
            cls.driver = webdriver.Remote(
                command_executor='http://localhost:4444/wd/hub',
                desired_capabilities=desired_capabilities
            )

        cls.driver.implicitly_wait(1)
        cls.driver.get('http://127.0.0.1:' + PORT + '/index.html')

    def test_1200(self):
        self.driver.set_window_size(1400, 1000)
        products = self.driver.find_elements_by_class_name('product')
        product = products[0]
        self.assertEqual(325, product.rect['width'])

    def test_850(self):
        self.driver.set_window_size(996, 1000)
        products = self.driver.find_elements_by_class_name('product')
        product = products[0]
        self.assertEqual(305, product.rect['width'])

    def test_650(self):
        self.driver.set_window_size(676, 1000)
        products = self.driver.find_elements_by_class_name('product')
        product = products[0]
        self.assertEqual(300, product.rect['width'])

    def test_under_650(self):
        self.driver.set_window_size(649, 1000)
        products = self.driver.find_elements_by_class_name('product')
        product = products[0]
        self.assertEqual(594, product.rect['width'])

    def test_background_body(self):
        container = self.driver.find_element_by_tag_name('body')
        background = str(container.value_of_css_property(
            'background-color')).replace(' ', '')
        result = ["rgba(250,250,250,1)", "#fafafaff"]
        self.assertIn(background, result)

    def test_background_buttons(self):
        buttons = self.driver.find_elements_by_link_text('نمایش')
        result = ["rgba(240,46,8,1)", "#f02e08ff"]
        for item in buttons:
            background = str(item.value_of_css_property(
                'background-color')).replace(' ', '')
            self.assertIn(background, result)

    def test_background_products(self):
        products = self.driver.find_elements_by_class_name('product')
        result = ["rgba(26,26,26,1)", "#1a1a1aff"]
        for item in products:
            background = str(item.value_of_css_property(
                'background-color')).replace(' ', '')
            self.assertIn(background, result)

    def test_product_border_radius(self):
        products = self.driver.find_elements_by_class_name('product')
        result = ["10px"]
        for item in products:
            border_radius = str(item.value_of_css_property(
                'border-radius')).replace(' ', '')
            self.assertIn(border_radius, result)

    def test_product_padding(self):
        products = self.driver.find_elements_by_class_name('product')
        result = ["10px"]
        for item in products:
            border_radius = str(item.value_of_css_property(
                'padding')).replace(' ', '')
            self.assertIn(border_radius, result)

    def test_product_image_width(self):
        products = self.driver.find_elements_by_tag_name('img')
        result = ["100px"]
        for item in products:
            width = str(item.value_of_css_property(
                'width')).replace(' ', '')
            self.assertIn(width, result)

    def test_product_image_max_width(self):
        products = self.driver.find_elements_by_tag_name('img')
        result = ["100%"]
        for item in products:
            max_width = str(item.value_of_css_property(
                'max-width')).replace(' ', '')
            self.assertIn(max_width, result)

    def test_product_button_padding(self):
        buttons = self.driver.find_elements_by_tag_name('a')
        result = ["5px15px5px15px", "5px15px"]
        for item in buttons:
            padding = str(item.value_of_css_property(
                'padding')).replace(' ', '')
            self.assertIn(padding, result)

    def test_product_button_text_decoration(self):
        buttons = self.driver.find_elements_by_tag_name('a')
        result = ["nonesolidrgb(250,250,250)"]
        for item in buttons:
            text_decoration = str(item.value_of_css_property(
                'text-decoration')).replace(' ', '')
            self.assertIn(text_decoration, result)

    def test_font(self):
        buttons = self.driver.find_elements_by_tag_name('a')
        result = "samim"
        for item in buttons:
            hover = ActionChains(self.driver).move_to_element(item)
            hover.perform()
            text_decoration = str(item.value_of_css_property(
                'font-family')).replace(' ', '').lower()
            self.assertTrue(result in text_decoration)

    @classmethod
    def tearDownClass(cls):
        console_logs = []
        for log_item in cls.driver.get_log('browser'):
            if log_item.get('source') == 'network' and 'favicon.ico - Failed to load' in log_item.get('message'):
                continue
            console_logs.append(log_item)
        if console_logs:
            print('\n--------------------\nBROWSER CONSOLE LOG:\n-----',
                  file=sys.stderr)
            for log_item in console_logs[:10]:
                log_item['message'] = log_item['message'][:200]
                print(pprint.pformat(log_item), '-----',
                      sep='\n', file=sys.stderr)
                cls.server.kill()
                cls.driver.close()


if __name__ == '__main__':
    unittest.main()
