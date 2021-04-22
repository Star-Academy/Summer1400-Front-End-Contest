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
                desired_capabilities=desired_capabilities,
            )

        cls.driver.get('http://127.0.0.1:' + PORT + '/index.html')

    def test_button_disabled(self):
        start_button = self.driver.find_element_by_id('start-button')
        before = start_button.get_attribute('disabled')
        self.assertIsNone(before)
        start_button.click()
        after = start_button.get_attribute('disabled')
        self.assertTrue(after)

    def test_lights(self):
        start_button = self.driver.find_element_by_id('start-button')
        start_button.click()
        wait = WebDriverWait(self.driver, 10)
        wait.until(EC.visibility_of_element_located((By.CSS_SELECTOR, ".off")))
        delay(.4)
        lights = get_lights(self)
        self.assertNotIn('off', lights['top-green'].get_attribute("class"))
        self.assertIn('off', lights['right-green'].get_attribute("class"))
        self.assertIn('off', lights['bottom-green'].get_attribute("class"))
        self.assertIn('off', lights['left-green'].get_attribute("class"))
        wait.until(EC.visibility_of_element_located((By.CSS_SELECTOR, ".screen--top>.light--green.off")))
        self.assertNotIn('off', lights['top-yellow'].get_attribute("class"))
        self.assertIn('off', lights['right-yellow'].get_attribute("class"))
        self.assertIn('off', lights['bottom-yellow'].get_attribute("class"))
        self.assertIn('off', lights['left-yellow'].get_attribute("class"))
        wait.until(EC.visibility_of_element_located((By.CSS_SELECTOR, ".screen--top>.light--yellow.off")))
        self.assertNotIn('off', lights['top-red'].get_attribute("class"))
        self.assertIn('off', lights['right-red'].get_attribute("class"))
        self.assertNotIn('off', lights['bottom-red'].get_attribute("class"))
        self.assertNotIn('off', lights['left-red'].get_attribute("class"))
        wait.until(EC.visibility_of_element_located((By.CSS_SELECTOR, ".screen--right>.light--green.off")))
        self.assertNotIn('off', lights['right-yellow'].get_attribute("class"))
        self.assertIn('off', lights['right-red'].get_attribute("class"))
        self.assertIn('off', lights['right-green'].get_attribute("class"))
        wait.until(EC.visibility_of_element_located((By.CSS_SELECTOR, ".screen--right>.light--yellow.off")))
        self.assertNotIn('off', lights['right-red'].get_attribute("class"))
        self.assertIn('off', lights['right-yellow'].get_attribute("class"))
        self.assertIn('off', lights['right-green'].get_attribute("class"))
        wait.until(EC.visibility_of_element_located((By.CSS_SELECTOR, ".screen--bottom>.light--green.off")))
        self.assertIn('off', lights['bottom-red'].get_attribute("class"))
        self.assertNotIn('off', lights['bottom-yellow'].get_attribute("class"))
        self.assertIn('off', lights['bottom-green'].get_attribute("class"))
        wait.until(EC.visibility_of_element_located((By.CSS_SELECTOR, ".screen--bottom>.light--yellow.off")))
        self.assertNotIn('off', lights['bottom-red'].get_attribute("class"))
        self.assertIn('off', lights['bottom-yellow'].get_attribute("class"))
        self.assertIn('off', lights['bottom-green'].get_attribute("class"))
        wait.until(EC.visibility_of_element_located((By.CSS_SELECTOR, ".screen--left>.light--green.off")))
        self.assertIn('off', lights['left-red'].get_attribute("class"))
        self.assertNotIn('off', lights['left-yellow'].get_attribute("class"))
        self.assertIn('off', lights['left-green'].get_attribute("class"))
        wait.until(EC.visibility_of_element_located((By.CSS_SELECTOR, ".screen--left>.light--yellow.off")))
        self.assertNotIn('off', lights['left-red'].get_attribute("class"))
        self.assertIn('off', lights['left-yellow'].get_attribute("class"))
        self.assertIn('off', lights['left-green'].get_attribute("class"))
        wait.until(EC.visibility_of_element_located((By.CSS_SELECTOR, ".screen--top>.light--green.off")))
        self.assertIn('off', lights['top-red'].get_attribute("class"))
        self.assertNotIn('off', lights['top-yellow'].get_attribute("class"))
        self.assertIn('off', lights['top-green'].get_attribute("class"))



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

def get_lights(test: SimpleTest) -> dict:
    return {
        'top-red': test.driver.find_element_by_css_selector('.screen--top>.light--red'),
        'top-yellow': test.driver.find_element_by_css_selector('.screen--top>.light--yellow'),
        'top-green': test.driver.find_element_by_css_selector('.screen--top>.light--green'),
        'right-red': test.driver.find_element_by_css_selector('.screen--right>.light--red'),
        'right-yellow': test.driver.find_element_by_css_selector('.screen--right>.light--yellow'),
        'right-green': test.driver.find_element_by_css_selector('.screen--right>.light--green'),
        'bottom-red': test.driver.find_element_by_css_selector('.screen--bottom>.light--red'),
        'bottom-yellow': test.driver.find_element_by_css_selector('.screen--bottom>.light--yellow'),
        'bottom-green': test.driver.find_element_by_css_selector('.screen--bottom>.light--green'),
        'left-red': test.driver.find_element_by_css_selector('.screen--left>.light--red'),
        'left-yellow': test.driver.find_element_by_css_selector('.screen--left>.light--yellow'),
        'left-green': test.driver.find_element_by_css_selector('.screen--left>.light--green')
    }

def delay(secs):
    time.sleep(secs)
    sys.stdout.flush()

if __name__ == '__main__':
    unittest.main()
