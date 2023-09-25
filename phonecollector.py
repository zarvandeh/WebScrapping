#----------------------------------------------------------Import Necessary libraries for work----------------------------------#
import random
import numpy
import pandas
import requests
from bs4 import BeautifulSoup
import lxml
from lxml import etree
import time
delay=4
### Setting of the scrapping project
mainpage="https://www.rond.ir"
pagination="https://www.rond.ir/SearchSim/Irancell?page="
lastpage=100
### Setting of the Category page
aclass="t-btn"
contactbuttonselector='a.t-btn'
### Setting of the contact page
sellernameclass='sstd'
nameselector='#layoutContent > div.t-page > div.grid_9.contactgrid > div.rtl.simInfo > table.stable>tr>td.sstd'
phoneclass='td.ltr'
#----------------------------------------GET User Agent Function-------------------------------------------------------------------#
def GET_UA():
    uastrings = ["Mozilla/5.0 (Windows NT 6.1; WOW64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/38.0.2125.111 Safari/537.36",
                 "Mozilla/5.0 (Windows NT 6.1; WOW64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/28.0.1500.72 Safari/537.36",
                 "Mozilla/5.0 (Macintosh; Intel Mac OS X 10_10) AppleWebKit/600.1.25 (KHTML, like Gecko) Version/8.0 Safari/600.1.25",
                 "Mozilla/5.0 (Windows NT 6.1; WOW64; rv:33.0) Gecko/20100101 Firefox/33.0",
                 "Mozilla/5.0 (Windows NT 6.3; WOW64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/38.0.2125.111 Safari/537.36",
                 "Mozilla/5.0 (Macintosh; Intel Mac OS X 10_10_0) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/38.0.2125.111 Safari/537.36",
                 "Mozilla/5.0 (Macintosh; Intel Mac OS X 10_9_5) AppleWebKit/600.1.17 (KHTML, like Gecko) Version/7.1 Safari/537.85.10",
                 "Mozilla/5.0 (Windows NT 6.1; WOW64; Trident/7.0; rv:11.0) like Gecko",
                 "Mozilla/5.0 (Windows NT 6.3; WOW64; rv:33.0) Gecko/20100101 Firefox/33.0",
                 "Mozilla/5.0 (Windows NT 6.1; WOW64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/38.0.2125.104 Safari/537.36"]
    return random.choice(uastrings)
#-------------------------------------Parse URL into Soup Object ------------------------------------------------------------------#
def parse_url(url):
    print(f'Fetching Data in {delay} seconds')
    time.sleep(delay)
    headers = {'User-Agent': GET_UA()}
    content = None
    try:
        response = requests.get(url, headers=headers)
        ct = response.headers['Content-Type'].lower().strip()
        if 'text/html' in ct:
            content = response.content
            soup = BeautifulSoup(content, "lxml")
        else:
            content = response.content
            soup = None
 
    except Exception as e:
        print(f'Error:, {str(e)}')
    print('Content successfully generated')
    return soup
#-------------------------------------------Scrap Single page information from URL-----------------------------------------------#
def scrap_info_page(url):
    soup=parse_url(url)
    name=soup.css.select_one(nameselector).text.strip()
    phones=soup.css.select(phoneclass)
    phone_numbers=[]
    for phone in phones:
        if len(phone.string.strip())>1:
            phone_numbers.append(phone.string.replace(" ", "").strip())
    userinfo=dict(username=name,usercontacts=phone_numbers)
    return userinfo
##--------------------collecting links from pagination pages ---------------------------------------------------------------------#
def remove_duplicates(list1):
  """Removes duplicate items from a list based on the text after "?id=".

  Args:
    list1: A list of strings.

  Returns:
    A list of strings with the duplicates removed.
  """

  # Create a set to store the unique items.
  unique_items = set()
  uniques=[]
  # Iterate over the list and add each item to the set if it is not already
  # present.
  for item in list1:
    id_split = item.split("?id=")
    id_part = id_split[1] if len(id_split) > 1 else ""
    if id_part not in unique_items:
      unique_items.add(id_part)
      uniques.append('https://www.rond.ir'+item)

  # Convert the set back to a list and return it.
  return uniques

#-----------------------------------------------Get a list of links inside the Catalogue page--------------------------------------#
def get_link_list(url):
    soup=parse_url(url)
    mylinks=soup.css.select('a.t-btn')
    mylinks=[x.get('href') for x in mylinks]
    umylinks=remove_duplicates(mylinks)
    return umylinks
#-----------------------------------------------Get all the links from Pagination navigation bar-----------------------------------#
#---------------------------------------------- Define the class --------------------------------------#

class rondirpage:
    def __init__(self):
        self.nameselector='#layoutContent > div.t-page > div.grid_9.contactgrid > div.rtl.simInfo > table.stable>tr>td.sstd'
        self.phoneclass = 'td.ltr'
        self.url=""
        self.delay=3
        
    def get_nameselector(self):
        return self.nameselector

    def set_nameselector(self, newselector):
        self.nameselector = newselector

    def get_phoneclass(self):
        return self.phoneclass

    def set_phoneclass(self, newphoneclass):
        self.phoneclass = newphoneclass
   
    def set_url(self):
        self.url = input('please enter your url')

    def getpageinfo(self):
        if self.url=="":
            print('| URL is not ste |')
        else:
            pageinfo=scrap_info_page(self.url,self.delay,self.nameselector,self.phoneclass)
            return pageinfo