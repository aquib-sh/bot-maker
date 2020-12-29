"""
Bot Class
Author: Shaikh Aquib

    Used for creating selenium bots without repeating the basic functions again and again.

    Param:
    - xpaths(dict)                    *dictionary xpath of all the elements present in operations*
    - data_file(string)(DEFAULT=None) *name of the file with data of links or anything, either xlsx or csv*

    Methods:       
    - setup_driver

"""

from selenium import webdriver
from selenium.webdriver.firefox.options import Options
from selenium.common.exceptions import NoSuchElementException, TimeoutException, StaleElementReferenceException
from selenium.webdriver.common.by import By
from selenium.webdriver.support.ui import WebDriverWait
from selenium.webdriver.support import expected_conditions as EC
import pandas as pd
import os
import sys


class BotMaker:

    def __init__(self, xpaths = None, data_file=None, behead=False):
        self.DATA_FILE = data_file
        self.df        = None
        self.XPATHS    = xpaths
        
        if self.DATA_FILE != None:
            # Create dataframe based on the file extension.
            self.temp = data_file.split(".")[1]
            if self.temp == "xlsx":
                self.df = pd.read_excel(self.DATA_FILE)
            elif self.temp == "csv":
                self.df = pd.read_csv(self.DATA_FILE)
            else:
                raise Exception("Unable to detect the file {}, please use either xlsx or csv file".format(self.DATA_FILE))
            del self.temp

        if self.XPATHS != None:
            if type(self.XPATHS) != dict:
                raise Exception("Xpaths must be a dictionary type")

        self.DEFAULT_WAIT = 10
        self.driver = None
        
        # Setup seleniumm webdriver based on current operating system.
        opts = Options()
        opts.headless = behead
        drivers_dir = os.path.join("resources","drivers")

        
        if sys.platform == "darwin":
            d_dir  = os.path.join(drivers_dir, "macos") 
            path   = os.path.join(d_dir,"geckodriver")
            self.driver = webdriver.Firefox(options=opts, executable_path = path, firefox_binary = "/Applications/Firefox.app/Contents/MacOS/firefox-bin")
        
        elif sys.platform == "linux":
            d_dir  = os.path.join(drivers_dir, "linux")  
            path   = os.path.join(d_dir, "geckodriver")
            self.driver = webdriver.Firefox(options=opts, executable_path = path, firefox_binary = "/usr/bin/firefox-esr")

        elif sys.platform == "win32":
            d_dir  = os.path.join(drivers_dir, "windows") 
            path   = os.path.join(d_dir, "geckodriver.exe")
            self.driver = webdriver.Firefox(options=opts, executable_path = path)
            
    # ============== Getters ==================
    def get_driver(self):
        return self.driver
    
    def get_data_frame(self):
        return self.df

    def get_xpath(self):
        return self.XPATHS

    def get_element(self, xpath, elem=None):      
        if elem != None:
            return WebDriverWait(elem, self.DEFAULT_WAIT).until(EC.presence_of_element_located((By.XPATH, xpath)))
        return WebDriverWait(self.driver, self.DEFAULT_WAIT).until(EC.presence_of_element_located((By.XPATH, xpath)))

    def get_elements(self, xpath, elem=None):
        if elem != None:
            return WebDriverWait(elem, self.DEFAULT_WAIT).until(EC.presence_of_element_located((By.XPATH, xpath)))
        return WebDriverWait(self.driver, self.DEFAULT_WAIT).until(EC.presence_of_all_elements_located((By.XPATH, xpath)))

    def get_element_by_id(self, id_, elem=None):
        if elem != None:
            return WebDriverWait(elem, self.DEFAULT_WAIT).until(EC.presence_of_element_located((By.ID, id_)))
        return WebDriverWait(self.driver, self.DEFAULT_WAIT).until(EC.presence_of_element_located((By.ID, id_)))

    def get_element_by_class(self, class_name, elem=None):
        if elem != None:
            return WebDriverWait(elem, self.DEFAULT_WAIT).until(EC.presence_of_element_located((By.CLASS_NAME, class_name)))
        return WebDriverWait(self.driver, self.DEFAULT_WAIT).until(EC.presence_of_element_located((By.CLASS_NAME, class_name)))

    # ============== Setters ==================
    def set_xpath(self, mod_xpath):
        self.XPATHS = mod_xpath

    # =============== Clickers ================
    def click_element(self, xpath, elem=None):
        """ Clicks an element. """
        if elem != None:
            WebDriverWait(elem, self.DEFAULT_WAIT).until(EC.presence_of_element_located((By.XPATH, xpath))).click()
        WebDriverWait(self.driver, self.DEFAULT_WAIT).until(EC.presence_of_element_located(
            (By.XPATH, xpath)
            )).click()

    def click_element_by_id(self, id_, elem=None):
        """ Clicks an element based on search by id. """ 
        if elem != None:
            WebDriverWait(elem, self.DEFAULT_WAIT).until(EC.presence_of_element_located((By.ID, id_))).click()
        WebDriverWait(self.driver, self.DEFAULT_WAIT).until(EC.presence_of_element_located(
            (By.ID, id_)
            )).click()

    def click_element_by_css_selector(self, selector, elem=None):
        """ Clicks an element based on search by id. """
        if elem != None:
            WebDriverWait(elem, self.DEFAULT_WAIT).until(EC.presence_of_element_located((By.CSS_SELECTOR, selector))).click()
        WebDriverWait(self.driver, self.DEFAULT_WAIT).until(EC.presence_of_element_located(
            (By.CSS_SELECTOR, selector)
            )).click()

    def click_interactable_element(self, selector, elem=None):
        if elem != None:
            WebDriverWait(elem, self.DEFAULT_WAIT).until(EC.element_to_be_clickable((By.CSS_SELECTOR, selector))).click()
        WebDriverWait(self.driver, self.DEFAULT_WAIT).until(EC.element_to_be_clickable(
            (By.CSS_SELECTOR, selector)
            )).click()
    # =========================================
    def move(self, link):
        self.driver.get(link)

    def upload_keys(self, xpath, key_data):
        """ Sends key to the input element. """
        WebDriverWait(self.driver, self.DEFAULT_WAIT).until(EC.presence_of_element_located(
            (By.XPATH, xpath)
            )).send_keys(key_data)

    def page_source(self):
        return self.driver.page_source

    def execute_script(self, command):
        return self.driver.execute_script(command)

    def shutdown(self):
        self.driver.quit()


