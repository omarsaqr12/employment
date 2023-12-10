# Imports
import requests
import selenium
import parsel
import pandas as pd
from datetime import date
from datetime import timedelta
import time
from parsel import Selector
from selenium import webdriver
from selenium.webdriver.chrome.service import Service as ChromeService
from webdriver_manager.chrome import ChromeDriverManager
from selenium.webdriver.support.select import Select
from selenium.webdriver.common.by import By
from selenium.webdriver.chrome.options import Options
from selenium.webdriver.support.ui import WebDriverWait
from selenium.webdriver.support import expected_conditions as EC
from bs4 import BeautifulSoup
import re
# configure webdriver
options = Options()
options.add_argument("--headless")  # hide GUI
options.add_argument("--window-size=1920,1080")  # set window size to native GUI size
options.add_argument("start-maximized")  # ensure window is full-screen
# configure chrome browser to not load images and javascript
options.add_experimental_option(
    "prefs", {"profile.managed_default_content_settings.images": 2}
)
driver = webdriver.Chrome(service=ChromeService(ChromeDriverManager().install()))
driver.get("https://wuzzuf.net/jobs/p/MLFshwbLgZbJ-Technical-Director-DAF-Holding-Cairo-Egypt?o=67&l=bp&t=bj&bpv=np&a=IT-Software-Development-Jobs-in-Egypt")
soup = BeautifulSoup(driver.page_source,features="lxml")
#the following 4 functions are responsible for experience, career level, education level, and salary


def get_experience2(soup):
    # ideally there sould be 4 spans experience, career level, education level, and salary, also for the experience span there are for possible scenarios, 3, more than 3, 3 to 5, and Not Specified
    init_string = soup.select("span.css-47jx3m > span")[0].text.split(' ')
    if (init_string[0] == "Not"):
        return [None,None]
    elif (len(init_string[0])>1 and init_string[0]== "More"):    
        MinMaxExp = [init_string[2],None]
    elif (len(init_string) == 1):
        MinMaxExp = [init_string[0],init_string[0]]
    else:
        MinMaxExp = [init_string[0],init_string[2]]
    print(MinMaxExp)
    return MinMaxExp
def get_career(soup):
    init_string = soup.select("span.css-47jx3m > span")[1].text
    if (init_string == "Not Specified" or init_string == "Not specified "):
            print(0)
            return None
    else:
         print(init_string)
         return init_string
def get_education(soup):
    init_string = soup.select("span.css-47jx3m > span")[2].text
    if (init_string == "Not Specified" or init_string == "Not specified "):
            print(0)
            return None
    else:
         print(init_string)
         return init_string
def get_salary(soup):
    init_string = soup.select("span.css-47jx3m > span")[3].text
    if (init_string == "Confidential" or init_string == "Confidential "):
            print(0)
            return None
    else:
         print(init_string)
         return init_string
    


get_experience2(soup)
get_career(soup)
get_education(soup)
get_salary(soup)