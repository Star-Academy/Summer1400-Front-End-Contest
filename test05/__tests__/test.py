import os
import pprint
import re
import subprocess
import sys
import signal
import unittest
import time
from unittest.util import three_way_cmp

from selenium import webdriver
from selenium.webdriver.common.desired_capabilities import DesiredCapabilities
from selenium.webdriver.common.by import By
from selenium.webdriver.support.ui import WebDriverWait
from selenium.webdriver.support import expected_conditions as EC
from selenium.webdriver.common.action_chains import ActionChains
from selenium.webdriver.common.keys import Keys
import time

DEBUG = 'PRODUCTION' not in os.environ

SRC_PATH = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))
PORT = '5503'


class SimpleTest(unittest.TestCase):
    nodeServer = ''

    @classmethod
    def setUp(cls):
        print('DEBUG = {}'.format(DEBUG), file=sys.stderr)
        cls.server = subprocess.Popen(
            ['python3', '-m', 'http.server', PORT], cwd=SRC_PATH, stderr=subprocess.DEVNULL)

        desired_capabilities = dict(
            {'loggingPrefs': {'browser': 'ALL'}}, **DesiredCapabilities.CHROME)

        if DEBUG:
            cls.driver = webdriver.Chrome(
                executable_path="D:\ChromeDriver\chromedriver.exe", desired_capabilities=desired_capabilities)
        else:
            cls.driver = webdriver.Remote(
                command_executor='http://localhost:4444/wd/hub',
                desired_capabilities=desired_capabilities
            )

        cls.driver.implicitly_wait(10)
        cls.driver.get('http://127.0.0.1:' + PORT + '/index.html')

        cls.nodeServer = subprocess.Popen(['npm', 'run', 'server'], cwd=SRC_PATH, stderr=subprocess.DEVNULL,
                                          shell=True)

    def test_button_disabled(self):
        start_button = self.driver.find_element_by_id('start-button')
        before = start_button.get_attribute('disabled')
        self.assertIsNone(before)
        start_button.click()
        after = start_button.get_attribute('disabled')
        self.assertTrue(after)

    def test_top_green(self):
        start_button = self.driver.find_element_by_id('start-button')
        light = self.driver.find_element_by_css_selector(
            '.screen--top>.light--green')
        check_green(self, light, start_button, 0, 1, 1, 6)

    def test_top_yellow(self):
        start_button = self.driver.find_element_by_id('start-button')
        light = self.driver.find_element_by_css_selector(
            '.screen--top>.light--yellow')
        check_yellow(self, light, start_button, 0, 1, 1, 6)

    def test_top_red(self):
        start_button = self.driver.find_element_by_id('start-button')
        light = self.driver.find_element_by_css_selector(
            '.screen--top>.light--red')
        check_red(self, light, start_button, 0, 1, 1, 6)

    def test_right_green(self):
        start_button = self.driver.find_element_by_id('start-button')
        light = self.driver.find_element_by_css_selector(
            '.screen--right>.light--green')
        check_green(self, light, start_button, 2, 1, 1, 4)

    def test_right_yellow(self):
        start_button = self.driver.find_element_by_id('start-button')
        light = self.driver.find_element_by_css_selector(
            '.screen--right>.light--yellow')
        check_yellow(self, light, start_button, 2, 1, 1, 4)

    def test_right_red(self):
        start_button = self.driver.find_element_by_id('start-button')
        light = self.driver.find_element_by_css_selector(
            '.screen--right>.light--red')
        check_red(self, light, start_button, 2, 1, 1, 4)

    def test_bottom_green(self):
        start_button = self.driver.find_element_by_id('start-button')
        light = self.driver.find_element_by_css_selector(
            '.screen--bottom>.light--green')
        check_green(self, light, start_button, 4, 1, 1, 2)

    def test_bottom_yellow(self):
        start_button = self.driver.find_element_by_id('start-button')
        light = self.driver.find_element_by_css_selector(
            '.screen--bottom>.light--yellow')
        check_yellow(self, light, start_button, 4, 1, 1, 2)

    def test_bottom_red(self):
        start_button = self.driver.find_element_by_id('start-button')
        light = self.driver.find_element_by_css_selector(
            '.screen--bottom>.light--red')
        check_red(self, light, start_button, 4, 1, 1, 2)

    def test_left_green(self):
        start_button = self.driver.find_element_by_id('start-button')
        light = self.driver.find_element_by_css_selector(
            '.screen--left>.light--green')
        check_green(self, light, start_button, 6, 1, 1, 0)

    def test_left_yellow(self):
        start_button = self.driver.find_element_by_id('start-button')
        light = self.driver.find_element_by_css_selector(
            '.screen--left>.light--yellow')
        check_yellow(self, light, start_button, 6, 1, 1, 0)

    def test_left_red(self):
        start_button = self.driver.find_element_by_id('start-button')
        light = self.driver.find_element_by_css_selector(
            '.screen--left>.light--red')
        check_red(self, light, start_button, 6, 1, 1, 0)

    @classmethod
    def tearDown(cls):
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
        os.kill(os.getpgid(cls.nodeServer.pid), signal.SIGTERM)
        cls.driver.close()


def check_green(test: SimpleTest, light, start_button, red1: int, green: int, yellow: int, red2):
    classes = light.get_attribute("class")
    test.assertNotIn('off', classes)
    start_button.click()
    time.sleep(2.5)
    time.sleep(red1)
    classes = light.get_attribute("class")
    test.assertNotIn('off', classes)
    time.sleep(green)
    classes = light.get_attribute("class")
    test.assertIn('off', classes)
    time.sleep(yellow)
    classes = light.get_attribute("class")
    test.assertIn('off', classes)
    time.sleep(red2 / 2.0)
    classes = light.get_attribute("class")
    test.assertIn('off', classes)
    time.sleep(red1 + red2 / 2.0)
    classes = light.get_attribute("class")
    test.assertNotIn('off', classes)

def check_yellow(test: SimpleTest, light, start_button, red1: int, green: int, yellow: int, red2):
    classes = light.get_attribute("class")
    test.assertNotIn('off', classes)
    start_button.click()
    time.sleep(2.5)
    time.sleep(red1)
    classes = light.get_attribute("class")
    test.assertIn('off', classes)
    time.sleep(green)
    classes = light.get_attribute("class")
    test.assertNotIn('off', classes)
    time.sleep(yellow)
    classes = light.get_attribute("class")
    test.assertIn('off', classes)
    time.sleep(red2 / 2.0)
    classes = light.get_attribute("class")
    test.assertIn('off', classes)
    time.sleep(red2 / 2.0)
    classes = light.get_attribute("class")
    test.assertIn('off', classes)
    time.sleep(red1)
    classes = light.get_attribute("class")
    test.assertIn('off', classes)
    time.sleep(green)
    classes = light.get_attribute("class")
    test.assertNotIn('off', classes)

def check_red(test: SimpleTest, light, start_button, red1: int, green: int, yellow: int, red2):
    classes = light.get_attribute("class")
    test.assertNotIn('off', classes)
    start_button.click()
    time.sleep(2.5)
    time.sleep(red1)
    classes = light.get_attribute("class")
    test.assertIn('off', classes)
    time.sleep(green)
    classes = light.get_attribute("class")
    test.assertIn('off', classes)
    time.sleep(yellow)
    classes = light.get_attribute("class")
    test.assertNotIn('off', classes)
    time.sleep(red2 / 2.0)
    classes = light.get_attribute("class")
    test.assertNotIn('off', classes)
    time.sleep(red1 + red2 / 2.0)
    classes = light.get_attribute("class")
    test.assertIn('off', classes)

if __name__ == '__main__':
    unittest.main()
