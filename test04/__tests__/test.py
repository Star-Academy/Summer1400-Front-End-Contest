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
PORT = '5500'


class SimpleTest(unittest.TestCase):
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

    def test_change_text(self):
        title = self.driver.find_element_by_id('title')
        hello_button = self.driver.find_element_by_id('hello-button')
        before = title.text
        self.assertEqual(before, "...")
        hello_button.click()
        time.sleep(.2)
        after = title.text
        self.assertEqual(after, 'Hello, Code-Star!')

    def test_change_color(self):
        color_button = self.driver.find_element_by_id('color-button')
        item = self.driver.find_element_by_tag_name('body')

        time.sleep(.2)
        background1 = str(item.value_of_css_property(
            'background-color')).replace(' ', '')
        self.assertEqual(background1, "rgba(26,26,26,1)")

        color_button.click()
        time.sleep(.2)
        background2 = str(item.value_of_css_property(
            'background-color')).replace(' ', '')
        self.assertEqual(background2, "rgba(240,46,8,1)")

        color_button.click()
        time.sleep(.2)
        background3 = str(item.value_of_css_property(
            'background-color')).replace(' ', '')
        self.assertEqual(background3, "rgba(14,56,161,1)")

        color_button.click()
        time.sleep(.2)
        background4 = str(item.value_of_css_property(
            'background-color')).replace(' ', '')
        self.assertEqual(background4, "rgba(240,46,8,1)")

        color_button.click()
        time.sleep(.2)
        background5 = str(item.value_of_css_property(
            'background-color')).replace(' ', '')
        self.assertEqual(background5, "rgba(14,56,161,1)")

    def test_change_color_and_change_text(self):
        title = self.driver.find_element_by_id('title')
        color_button = self.driver.find_element_by_id('color-button')
        hello_button = self.driver.find_element_by_id('hello-button')

        item = self.driver.find_element_by_tag_name('body')
        background1 = str(item.value_of_css_property(
            'background-color')).replace(' ', '')
        self.assertEqual(background1, "rgba(26,26,26,1)")

        color_button.click()
        time.sleep(.2)
        background2 = str(item.value_of_css_property(
            'background-color')).replace(' ', '')
        self.assertEqual(background2, "rgba(240,46,8,1)")
        before = title.text
        self.assertEqual(before, "...")

        hello_button.click()
        time.sleep(.2)
        after = title.text
        self.assertEqual(after, 'Hello, Code-Star!')

        background2 = str(item.value_of_css_property(
            'background-color')).replace(' ', '')
        self.assertEqual(background2, "rgba(240,46,8,1)")

        color_button.click()
        time.sleep(.2)
        background3 = str(item.value_of_css_property(
            'background-color')).replace(' ', '')
        self.assertEqual(background3, "rgba(14,56,161,1)")

        color_button.click()
        time.sleep(.2)
        background4 = str(item.value_of_css_property(
            'background-color')).replace(' ', '')
        self.assertEqual(background4, "rgba(240,46,8,1)")

        color_button.click()
        time.sleep(.2)
        background5 = str(item.value_of_css_property(
            'background-color')).replace(' ', '')
        self.assertEqual(background5, "rgba(14,56,161,1)")

    def test_load_js(self):
        result = self.driver.execute_script("return colors")
        self.assertEqual(result, ['#f02e08', '#0e38a1'])

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
                cls.driver.close()


if __name__ == '__main__':
    unittest.main()
