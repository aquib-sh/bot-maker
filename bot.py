""" Bot Class
    Author: Shaikh Aquib
    
        Helps in simplyifiying the complex logic and repeatitive tasks in selenium library.
"""

import os
import sys
import time
import random
import undetected_chromedriver.v2 as uc
import seleniumwire.webdriver as wired_webdriver
from selenium import webdriver
from selenium.webdriver.firefox.options import Options
from selenium.common.exceptions import NoSuchElementException
from selenium.common.exceptions import TimeoutException
from selenium.common.exceptions import StaleElementReferenceException
from selenium.webdriver.common.proxy import Proxy, ProxyType
from selenium.webdriver.common.desired_capabilities import DesiredCapabilities
from selenium.webdriver.common.by import By 
from selenium.webdriver.support import expected_conditions as EC
from selenium.webdriver.support.ui import WebDriverWait


class BotOptions:
    def setup_chrome(self, driver_path, behead, undetected=False, page_load_strategy=None, profile_path:str=None):
        """Returns Chrome Driver object depending on the parameters. 
        
        Parameters
        ----------
        driver_path: str
            Path of the webdriver executable_path
            
        behead: bool
            Whether to have headless browser or normal.
        
        undetected: bool (OPTIONAL DEFAULT=False)
            Whether to initialize undetected_chromedriver instead of chrome_driver
        
        load_profile: str (OPTIONAL DEFAULT=None)
            Path of the browser profile to use
        """
        opts = webdriver.ChromeOptions()
        opts.headless = behead
        
        if profile_path:
            opts.add_argument(f"user-data-dir={profile_path}")
            
        dpath = driver_path

        capa = None
        if page_load_strategy:
            capa = DesiredCapabilities.CHROME
            capa['pageLoadStrategy'] = page_load_strategy

        if sys.platform == "win32":
            dpath = os.path.abspath(dpath) + ".exe"
        if undetected : return uc.Chrome(options=opts, executable_path=dpath)
        return webdriver.Chrome(options=opts, executable_path=dpath, desired_capabilities=capa)

    def setup_firefox(self, driver_path, behead, proxy_info: dict=None, firefox_profile: str=None):
        """Returns Firefox Driver object depending on the parameters. 
        
        Parameters
        ----------
        driver_path: str
            Path of the webdriver executable_path
            
        behead: bool
            Whether to have headless browser or normal.
            
        proxy_info: dict (DEFAULT=None) (Optional)
            Information about the proxy to use (if want to)
            example of proxy_info dict given below:
            proxy_info = {
                'Username':'xyz',
                'Password':'123klu456',
                'PROXY IP:PORT (HTTP)':'ip_address:port_number',
            }
        
        firefox_profile: str (OPTIONAL DEFAULT=None)
            Path of the browser profile to use
        """
        opts = webdriver.FirefoxOptions()
        
        profile = None
        if firefox_profile:
            profile = webdriver.FirefoxProfile(firefox_profile) 
        else:
            profile = webdriver.FirefoxProfile()
            
        profile.set_preference("dom.webdriver.enabled", False)
        profile.set_preference('useAutomationExtension', False)
        
        profile.update_preferences()
        desired = DesiredCapabilities.FIREFOX

        opts.headless = behead
        dpath = driver_path
        if sys.platform == "win32":
            dpath += ".exe"
        
        options = None
        if proxy_info:
            options = {
                'proxy':{
                    'http':f"http://{proxy_info['Username']}:{proxy_info['Password']}@{proxy_info['PROXY IP:PORT (HTTP)']}",
                    'https':f"https://{proxy_info['Username']}:{proxy_info['Password']}@{proxy_info['PROXY IP:PORT (HTTP)']}",
                }
            }
            return wired_webdriver.Firefox(options=opts, executable_path=dpath,
                firefox_profile=profile, desired_capabilities=desired, seleniumwire_options=options)

        return webdriver.Firefox(options=opts, executable_path=dpath,
                firefox_profile=profile, desired_capabilities=desired)

    def setup_edge(self, driver_path):
        dpath = driver_path
        if sys.platform == "win32":
            dpath += ".exe"
        return webdriver.Edge(executable_path=dpath)


class BotMaker:
    """BotMaker: Simplifies creating and using Selenium WebDriver

    Parameters
    ----------
    behead: bool (DEFAULT=False) (Optional)
        creates the bot in headless mode if set to True.

    browser: str (DEFAULT="Firefox")
        Browser to use for BotMaker.
        browser must be in ['Firefox', 'Chrome', 'Edge']

    undetected: bool (DEFAULT=False) (Optional)
        Uses the undetected_chromedriver instead of normal chrome driver, 
        This avoids the bot detection to a certain extent.
        (ONLY FOR GOOGLE CHROME)

    proxy_info: dict (DEFAULT=None) (Optional)
        Information about the proxy to use (if want to)
        example of proxy_info dict given below:
        proxy_info = {
            'Username':'xyz',
            'Password':'123klu456',
            'PROXY IP:PORT (HTTP)':'ip_address:port_number',
        }
        
    firefox_profile: str (OPTIONAL DEFAULT=None)
        Path of the browser profile to use
    """
    def __init__(self, behead=False, browser="Firefox", undetected=False, 
        page_load_strategy=None, load_profile:str=None, proxy_info:dict=None, firefox_profile:str=None):
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
            self.driver = bot_ops.setup_firefox(firefox_driver, behead, proxy_info=proxy_info, firefox_profile=firefox_profile)
        elif browser == "Edge":
            self.driver = bot_ops.setup_edge(edge_driver)
        elif browser == "Chrome":
            self.driver = bot_ops.setup_chrome(chrome_driver, behead, undetected=undetected, page_load_strategy=page_load_strategy, profile_path=load_profile)
        self.DEFAULT_WAIT = 10

    def move(self, link):
        """ Move on to certian link. """
        self.driver.get(link)

    def send_human_keys(element, _key):
        element.clear()
        for letter in _key:
            element.send_keys(letter)
            time.sleep(random.random())

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
            
    def get_interactable_element(self, xpath, elem=None):
        """ Waits for element to be interactable before clicking by xpath. """
        if elem != None:
            return WebDriverWait(elem, self.DEFAULT_WAIT).until(EC.element_to_be_clickable((By.XPATH, xpath)))
        return WebDriverWait(self.driver, self.DEFAULT_WAIT).until(EC.element_to_be_clickable(
            (By.XPATH, xpath)
            ))

    def get_interactable_element_by_css_selector(self, selector, elem=None):
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
