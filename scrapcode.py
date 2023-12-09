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
