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
driver.get("https://wuzzuf.net/jobs/p/hS5nz4CthTFG-Software-Developer-Misr-Elkheir-Foundation-Cairo-Egypt?o=2&l=bp&t=bj&bpv=np&a=IT-Software-Development-Jobs-in-Egypt")
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
    
def postdate(soup):
    Complete_area = soup.select("strong.css-9geu3q:nth-child(4)")[0].next_sibling.text.split(' ')
    Complete_area = [Complete_area[1],Complete_area[2]]
    print(Complete_area)
    return Complete_area
def numberofapplicants(soup):
    Complete_area = soup.select("strong.css-9geu3q:nth-child(4)")[0].next_sibling.next_sibling.text.split(' ')
    applicants=Complete_area[0].replace("Applicants","")
    vaccancies=Complete_area[1]
    vaccancies=vaccancies[-1]
    if(vaccancies=="-"):
         vaccancies=Complete_area[2]
    print(vaccancies)
    print(applicants)
    print(Complete_area)
def locationofcompandcompname(soup):
    Complete_area = soup.select("strong.css-9geu3q:nth-child(4)")[0].text.split(' ')
    companyname=""
    companylocation=""
    i=0
    if Complete_area[0]=="Confidential":
         companyname=None
    else:
         while Complete_area[i][0]!='-':
              companyname+=Complete_area[i]+" "
              i=i+1
    while i< len(Complete_area):
         companylocation+=Complete_area[i].replace("-\xa0","")
         i=i+1
    print(companylocation)
    print(companyname)
def JobDescandrequirments(soup):
     jobdescription=soup.select("html body div#app div main.css-44l6ak section.css-ghicub div.css-1uobp1k")[0].text
     jobreq=soup.select("html body div#app div main.css-44l6ak section.css-ghicub div.css-1t5f0fr")[0].text
     print(jobreq)
     print(jobdescription)
# now scrap from the company page 
def companywebisteandsocialmedialinks(soup):
     links=[]
     s=soup.select("html body div#app div div div.css-1cvvhv div.css-ku8yfm div.css-12e2e2p div.css-aqnjlk div.css-1517rho a.css-cttont")[0].get("href")
     links.append(s)
    #  print(soup.select("html body div#app div div div.css-1cvvhv div.css-ku8yfm div.css-12e2e2p div.css-aqnjlk div.css-18rpd7u"))
     for social in soup.select("html body div#app div div div.css-1cvvhv div.css-ku8yfm div.css-12e2e2p div.css-aqnjlk div.css-18rpd7u a"):
          links.append(social.get("href"))
     print(links)

def companylocation_industries_founded_compsize(soup):
     data=[]
     data.append(soup.select("html body div#app div div.css-1i3nj6 div#profile-section.css-yujkym.es4ywkp0 div.css-1mjtpgs span.css-1xhj18k span.css-16heon9")[0].text)
     data.append(soup.select("html body div#app div div.css-1i3nj6 div#profile-section.css-yujkym.es4ywkp0 div.css-1mjtpgs span.css-1xhj18k span.css-6whuzn")[0].text)
     data.append(soup.select("html body div#app div div.css-1i3nj6 div#profile-section.css-yujkym.es4ywkp0 div.css-1mjtpgs span.css-1xhj18k")[2].text)
     data.append(soup.select("html body div#app div div.css-1i3nj6 div#profile-section.css-yujkym.es4ywkp0 div.css-1mjtpgs span.css-1xhj18k")[3].text)
     s=soup.select("html body div#app div div.css-1i3nj6 div#profile-section.css-yujkym.es4ywkp0 p.css-1ceuc1v")[0].text
     x=(s[-4:-1])
     if x=="Mor":
          driver.find_element(By.CSS_SELECTOR, '#profile-section > p > span').click()
          soup2=BeautifulSoup(driver.page_source)
          s=soup2.select("html body div#app div div.css-1i3nj6 div#profile-section.css-yujkym.es4ywkp0 p.css-1ceuc1v")[0].text
          data.append(s[0:-10])

     else:
          data.append(s)

     print(data)
def getjobcategories(soup):
     data=set()
     s=soup.select(".css-s2o0yh")[0]
     spans=s.find_all("span")
     for w in spans:
          data.add(w.text)
     print(data)
def getcompanylink(soup):
     if soup.select(".css-p7pghv")==[]:
          print([])
     else:
          link=soup.select(".css-p7pghv")[0].get("href")
          print(link)

# get_experience2(soup)
# get_career(soup)
# get_education(soup)
# get_salary(soup)
# postdate(soup)
# locationofcompandcompname(soup)
# companylocation_industries_founded_compsize(soup)
# JobDescandrequirments(soup)
# getjobcategories(soup)
getcompanylink(soup)