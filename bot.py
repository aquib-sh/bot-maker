""" Bot Class
    Author: Shaikh Aquib
    
        Helps in simplyifiying the complex logic and repeatitive tasks in selenium library.
"""

import os
import sys
from selenium import webdriver
from selenium.webdriver.firefox.options import Options
from selenium.common.exceptions import NoSuchElementException
from selenium.common.exceptions import TimeoutException
from selenium.common.exceptions import StaleElementReferenceException
from selenium.webdriver.common.desired_capabilities import DesiredCapabilities
from selenium.webdriver.common.by import By 
from selenium.webdriver.support import expected_conditions as EC
from selenium.webdriver.support.ui import WebDriverWait


class BotOptions:
    def setup_chrome(self, driver_path, behead, page_load_strategy=None):
        opts = webdriver.ChromeOptions()
        opts.headless = behead
        dpath = driver_path

        capa = None
        if page_load_strategy:
            capa = DesiredCapabilities.CHROME
            capa['pageLoadStrategy'] = page_load_strategy

        if sys.platform == "win32":
            dpath = os.path.abspath(dpath) + ".exe"
        return webdriver.Chrome(options=opts, executable_path=dpath, desired_capabilities=capa)

    def setup_firefox(self, driver_path, behead):
        opts = webdriver.FirefoxOptions()
        opts.headless = behead
        dpath = driver_path
        if sys.platform == "win32":
            dpath += ".exe"
        return webdriver.Firefox(options=opts, executable_path=dpath)

    def setup_edge(self, driver_path):
        dpath = driver_path
        if sys.platform == "win32":
            dpath += ".exe"
        return webdriver.Edge(executable_path=dpath)


class BotMaker:
    def __init__(self, behead=False, browser="Firefox", page_load_strategy=None):
        dir_driver = os.path.join("resources", "drivers")

        if sys.platform == "win32":
            dir_driver = os.path.join(dir_driver, "windows")
        elif sys.platform == "linux":
            dir_driver = os.path.join(dir_driver, "linux")
        elif sys.platform == "darwin":
            dir_driver = os.path.join(dir_driver, "macos")

        firefox_driver = os.path.join(dir_driver, "geckodriver")            
        edge_driver = os.path.join(dir_driver, "msedgedriver")
        chrome_driver = os.path.join(dir_driver, "chromedriver")

        bot_ops = BotOptions()

        self.driver = None
        if browser == "Firefox":
            self.driver = bot_ops.setup_firefox(firefox_driver, behead)
        elif browser == "Edge":
            self.driver = bot_ops.setup_edge(edge_driver)
        elif browser == "Chrome":
            self.driver = bot_ops.setup_chrome(chrome_driver, behead, page_load_strategy=page_load_strategy)
        self.DEFAULT_WAIT = 10

    def move(self, link):
        """ Move on to certian link. """
        self.driver.get(link)

    def upload_keys(self, xpath, key_data):
        """ Sends key to the input element by xpath. """
        WebDriverWait(self.driver, self.DEFAULT_WAIT).until(EC.presence_of_element_located(
            (By.XPATH, xpath)
            )).send_keys(key_data)
    
    def upload_keys_by_css_selector(self, selector, key_data):
        self.get_element_by_css_selector(selector).send_keys(key_data)

    def page_source(self):
        return self.driver.page_source

    def execute_script(self, command):
        return self.driver.execute_script(command)

    def shutdown(self):
        self.driver.quit()

    def create_wait(self, timeout):
        wait = WebDriverWait(self.driver, 20)
        return wait

    def wait_until_found_xpath(self, wait_obj, xpath):
        wait_obj.until(EC.presence_of_element_located((By.XPATH, xpath)))        

    def get_source(self, elem=None):
        if elem == None:
            elem = self.driver
        return elem.page_source

    def get_driver(self):
        """ Returns Driver. """
        return self.driver

    def get_element(self, xpath, elem=None):
        """ Return element by searching through Xpath. """      
        if elem != None:
            return WebDriverWait(elem, self.DEFAULT_WAIT).until(EC.presence_of_element_located((By.XPATH, xpath)))
        return WebDriverWait(self.driver, self.DEFAULT_WAIT).until(EC.presence_of_element_located((By.XPATH, xpath)))

    def get_element_by_id(self, id_, elem=None):
        """ Return element by searching through id. """
        if elem != None:
            return WebDriverWait(elem, self.DEFAULT_WAIT).until(EC.presence_of_element_located((By.ID, id_)))
        return WebDriverWait(self.driver, self.DEFAULT_WAIT).until(EC.presence_of_element_located((By.ID, id_)))

    def get_element_by_tag(self, tag, elem=None):
        """ Return element by searching through tag name. """
        if elem != None:
            return WebDriverWait(elem, self.DEFAULT_WAIT).until(EC.presence_of_element_located((By.TAG_NAME, tag)))
        return WebDriverWait(self.driver, self.DEFAULT_WAIT).until(EC.presence_of_element_located((By.TAG_NAME, tag)))

    def get_element_by_class(self, class_name, elem=None):
        """ Return element by searching through class name. """
        if elem != None:
            return WebDriverWait(elem, self.DEFAULT_WAIT).until(EC.presence_of_element_located((By.CLASS_NAME, class_name)))
        return WebDriverWait(self.driver, self.DEFAULT_WAIT).until(EC.presence_of_element_located((By.CLASS_NAME, class_name)))
    
    def get_element_by_css_selector(self, selector, elem=None):
        """ Return an element based on search by css selector. """
        if elem != None:
            return WebDriverWait(elem, self.DEFAULT_WAIT).until(EC.presence_of_element_located((By.CSS_SELECTOR, selector)))
        return WebDriverWait(self.driver, self.DEFAULT_WAIT).until(EC.presence_of_element_located(
            (By.CSS_SELECTOR, selector)
            ))
            
    def get_interactable_element(self, selector, elem=None):
        """ Waits for element to be interactable before clicking by css selector. """
        if elem != None:
            return WebDriverWait(elem, self.DEFAULT_WAIT).until(EC.element_to_be_clickable((By.CSS_SELECTOR, selector)))
        return WebDriverWait(self.driver, self.DEFAULT_WAIT).until(EC.element_to_be_clickable(
            (By.CSS_SELECTOR, selector)
            ))
        
    def get_elements(self, xpath, elem=None):
        """ Return a list of elements by searching through Xpath. """
        if elem != None:
            return WebDriverWait(elem, self.DEFAULT_WAIT).until(EC.presence_of_all_elements_located((By.XPATH, xpath)))
        return WebDriverWait(self.driver, self.DEFAULT_WAIT).until(EC.presence_of_all_elements_located((By.XPATH, xpath)))

    def get_elements_by_tag(self, tag, elem=None):
        """ Return elements by searching through tag name. """
        if elem != None:
            return WebDriverWait(elem, self.DEFAULT_WAIT).until(EC.presence_of_all_elements_located((By.TAG_NAME, tag)))
        return WebDriverWait(self.driver, self.DEFAULT_WAIT).until(EC.presence_of_all_elements_located((By.TAG_NAME, tag)))

    def get_elements_by_id(self, id_, elem=None):
        """ Return element by searching through id. """
        if elem != None:
            return WebDriverWait(elem, self.DEFAULT_WAIT).until(EC.presence_of_all_elements_located((By.ID, id_)))
        return WebDriverWait(self.driver, self.DEFAULT_WAIT).until(EC.presence_of_all_elements_located((By.ID, id_)))

    def get_elements_by_class(self, class_name, elem=None):
        """ Return element by searching through class name. """
        if elem != None:
            return WebDriverWait(elem, self.DEFAULT_WAIT).until(EC.presence_of_all_elements_located((By.CLASS_NAME, class_name)))
        return WebDriverWait(self.driver, self.DEFAULT_WAIT).until(EC.presence_of_all_elements_located((By.CLASS_NAME, class_name)))
    
    def get_elements_by_css_selector(self, selector, elem=None):
        """ Return an element based on search by css selector. """
        if elem != None:
            return WebDriverWait(elem, self.DEFAULT_WAIT).until(EC.presence_of_all_elements_located((By.CSS_SELECTOR, selector)))
        return WebDriverWait(self.driver, self.DEFAULT_WAIT).until(EC.presence_of_all_elements_located(
            (By.CSS_SELECTOR, selector)
            ))
