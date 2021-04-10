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
        self.driver.set_window_size(1250,1000)
        container = self.driver.find_element_by_tag_name('body')
        box = self.driver.find_element_by_id('logo')
        self.assertEqual(
            box.location['x'], container.rect['width'] / 2 - box.rect['width'] / 2)
        self.assertEqual(
            box.location['y'], container.rect['height'] / 2 - box.rect['height'] / 2)

    def test_color(self):
        container = self.driver.find_element_by_tag_name('body')
        background = str(container.value_of_css_property(
            'background-image')).replace(' ', '')
        result = ["linear-gradient(tobottomright,rgb(243,68,14),rgb(240,46,8))",
                  "linear-gradient(torightbottom,rgb(243,68,14),rgb(240,46,8))",
                  "linear-gradient(-45deg,rgb(243,68,14),rgb(240,46,8))",
                  "linear-gradient(315deg,rgb(243,68,14),rgb(240,46,8))"]
        self.assertIn(background, result)

    def test_width(self):
        box = self.driver.find_element_by_id('logo')
        background = str(box.value_of_css_property(
            'width'))
        result = ["100px"]

        self.assertIn(background, result)

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
