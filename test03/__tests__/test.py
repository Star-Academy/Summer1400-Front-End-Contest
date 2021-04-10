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
PORT = '5501'


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
                executable_path="D:\ChromeDriver\chromedriver.exe", desired_capabilities=desired_capabilities)
        else:
            cls.driver = webdriver.Remote(
                command_executor='http://localhost:4444/wd/hub',
                desired_capabilities=desired_capabilities
            )

        cls.driver.implicitly_wait(1)
        cls.driver.get('http://127.0.0.1:' + PORT + '/index.html')

    def test_position_logo(self):
        container = self.driver.find_element_by_class_name('logo')
        position = str(container.value_of_css_property(
            'position')).replace(' ', '')
        result = ["absolute"]
        self.assertIn(position, result)

    def test_top_logo(self):
        container = self.driver.find_element_by_class_name('logo')
        top = str(container.value_of_css_property(
            'top')).replace(' ', '')
        result = ["170px"]
        self.assertIn(top, result)

    def test_position_tag(self):
        tags = self.driver.find_elements_by_class_name('tag')
        result = ["absolute"]
        for tag in tags:
            value = str(tag.value_of_css_property(
                'position')).replace(' ', '')
            self.assertIn(value, result)

    def test_padding_left_tag(self):
        tags = self.driver.find_elements_by_class_name('tag')
        result = ["30px"]
        for tag in tags:
            top = str(tag.value_of_css_property(
                'padding-left')).replace(' ', '')
            self.assertIn(top, result)

    def test_font_size_tag(self):
        tags = self.driver.find_elements_by_class_name('tag')
        result = ["108px"]
        for tag in tags:
            top = str(tag.value_of_css_property(
                'font-size')).replace(' ', '')
            self.assertIn(top, result)

    def test_font_weight_tag(self):
        tags = self.driver.find_elements_by_class_name('tag')
        result = ["700"]
        for tag in tags:
            value = str(tag.value_of_css_property(
                'font-weight')).replace(' ', '')
            self.assertIn(value, result)

    def test_letter_spacing_tag(self):
        tags = self.driver.find_elements_by_class_name('tag')
        result = ["-7px"]
        for tag in tags:
            value = str(tag.value_of_css_property(
                'letter-spacing')).replace(' ', '')
            self.assertIn(value, result)

    def test_transform_tag_1(self):
        tag = self.driver.find_element_by_css_selector(".tag:nth-child(1)")
        result = ["rotate(-90deg)", "rotate(270deg)",
                  "matrix(6.12323e-17,-1,1,6.12323e-17,0,0)"]
        value = str(tag.value_of_css_property(
            'transform')).replace(' ', '')
        self.assertIn(value, result)

    def test_transform_tag_2(self):
        tag = self.driver.find_element_by_css_selector(".tag:nth-child(2)")
        result = ["rotate(-18deg)", "rotate(342deg)",
                  "matrix(0.951057,-0.309017,0.309017,0.951057,0,0)"]
        value = str(tag.value_of_css_property(
            'transform')).replace(' ', '')
        self.assertIn(value, result)

    def test_transform_tag_3(self):
        tag = self.driver.find_element_by_css_selector(".tag:nth-child(3)")
        result = ["rotate(54deg)", "rotate(306deg)",
                  "matrix(0.587785,0.809017,-0.809017,0.587785,0,0)"]
        value = str(tag.value_of_css_property(
            'transform')).replace(' ', '')
        self.assertIn(value, result)

    def test_transform_tag_4(self):
        tag = self.driver.find_element_by_css_selector(".tag:nth-child(4)")
        result = ["rotate(126deg)", "rotate(-234deg)",
                  "matrix(-0.587785,0.809017,-0.809017,-0.587785,0,0)"]
        value = str(tag.value_of_css_property(
            'transform')).replace(' ', '')
        self.assertIn(value, result)

    def test_transform_tag_5(self):
        tag = self.driver.find_element_by_css_selector(".tag:nth-child(5)")
        result = ["rotate(198deg)", "rotate(-162deg)",
                  "matrix(-0.951057,-0.309017,0.309017,-0.951057,0,0)"]
        value = str(tag.value_of_css_property(
            'transform')).replace(' ', '')
        self.assertIn(value, result)

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
