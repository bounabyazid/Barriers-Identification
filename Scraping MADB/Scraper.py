import csv
import json
import pickle

from urllib.request import urlopen
from bs4 import BeautifulSoup, Comment

# imports
import pandas as pd
import os

from selenium.webdriver import Chrome
from selenium.webdriver.chrome.options import Options

from selenium import webdriver
from selenium.webdriver.firefox.options import Options

import pandas as pd

from ActiveSPS import urls


import sys  
from PySide.QtGui import *  
from PySide.QtCore import *
from PySide import QtGui, QtCore, QtWebKit
from PySide.QtWebKit import QWebPage  

from lxml import html 

SPSurls = 'https://madb.europa.eu/madb/sps_barriers_result.htm?isSps=true&sectors=5&sectors=6&sectors=7&sectors=8&sectors=9&sectors=10&sectors=11&sectors=12&sectors=13&sectors=14&sectors=15&sectors=16&sectors=17&sectors=18&sectors=19&sectors=20&sectors=32&sectors=21&sectors=22&sectors=33&sectors=23&sectors=24&sectors=25&sectors=26&sectors=27&sectors=28&sectors=29&sectors=30&sectors=1&sectors=2&sectors=3&sectors=4&sectors=31&measures=43&measures=44&measures=45&measures=46&measures=47&measures=48&measures=49&measures=50&measures=51&measures=52&measures=53&measures=54&measures=55&measures=56&measures=57&measures=58&measures=59&measures=60&measures=61&measures=62&measures=63&measures=64&measures=65&measures=66&measures=67&measures=68&measures=69&measures=70&measures=71&measures=72&measures=73&measures=74&measures=75&measures=76&measures=77&measures=78&measures=79&measures=80&measures=81&measures=82&measures=83&measures=84&measures=85&measures=86&measures=87&measures=88&countries=AD&countries=AE&countries=AF&countries=AM&countries=AO&countries=AR&countries=AT&countries=AU&countries=BA&countries=BD&countries=BE&countries=BG&countries=BO&countries=BR&countries=BW&countries=BY&countries=CA&countries=CH&countries=CL&countries=CM&countries=CN&countries=CO&countries=CY&countries=CZ&countries=DE&countries=DK&countries=DO&countries=DZ&countries=EC&countries=EE&countries=EG&countries=ES&countries=FI&countries=FR&countries=GB&countries=GR&countries=HK&countries=HR&countries=HU&countries=ID&countries=IE&countries=IL&countries=IN&countries=IQ&countries=IR&countries=IS&countries=IT&countries=JO&countries=JP&countries=KR&countries=KW&countries=KZ&countries=LB&countries=LT&countries=LU&countries=LV&countries=MA&countries=MD&countries=ME&countries=MT&countries=MX&countries=MY&countries=MZ&countries=NG&countries=NL&countries=NO&countries=NZ&countries=OM&countries=PA&countries=PE&countries=PH&countries=PK&countries=PL&countries=PT&countries=PY&countries=QA&countries=RO&countries=RS&countries=RU&countries=SA&countries=SE&countries=SG&countries=SI&countries=SK&countries=TH&countries=TN&countries=TR&countries=TW&countries=UA&countries=UG&countries=US&countries=UY&countries=UZ&countries=VE&countries=VN&countries=ZA&lastUpdated=ANYTIME&showOnlyNew=false&showOnlyResolved=false'
NonSPSurls = 'https://madb.europa.eu/madb/barriers_result.htm?isSps=&sectors=5&sectors=6&sectors=7&sectors=8&sectors=9&sectors=10&sectors=11&sectors=12&sectors=13&sectors=14&sectors=15&sectors=16&sectors=17&sectors=18&sectors=19&sectors=20&sectors=32&sectors=21&sectors=22&sectors=33&sectors=23&sectors=24&sectors=25&sectors=26&sectors=27&sectors=28&sectors=29&sectors=30&sectors=1&sectors=2&sectors=3&sectors=4&sectors=31&measures=100&measures=101&measures=102&measures=103&measures=104&measures=105&measures=106&measures=107&measures=108&measures=109&measures=110&measures=111&measures=112&measures=113&measures=114&measures=115&measures=116&measures=117&measures=118&measures=119&measures=120&measures=121&measures=164&measures=43&measures=44&measures=45&measures=46&measures=47&measures=48&measures=49&measures=50&measures=51&measures=52&measures=53&measures=54&measures=55&measures=56&measures=57&measures=58&measures=59&measures=60&measures=61&measures=62&measures=63&measures=64&measures=65&measures=66&measures=67&measures=68&measures=69&measures=70&measures=71&measures=72&measures=73&measures=74&measures=75&measures=76&measures=77&measures=78&measures=79&measures=80&measures=81&measures=82&measures=83&measures=84&measures=85&measures=86&measures=87&countries=AD&countries=AE&countries=AF&countries=AM&countries=AO&countries=AR&countries=AT&countries=AU&countries=BA&countries=BD&countries=BE&countries=BG&countries=BO&countries=BR&countries=BW&countries=BY&countries=CA&countries=CH&countries=CL&countries=CM&countries=CN&countries=CO&countries=CY&countries=CZ&countries=DE&countries=DK&countries=DO&countries=DZ&countries=EC&countries=EE&countries=EG&countries=ES&countries=FI&countries=FR&countries=GB&countries=GR&countries=HK&countries=HR&countries=HU&countries=ID&countries=IE&countries=IL&countries=IN&countries=IQ&countries=IR&countries=IS&countries=IT&countries=JO&countries=JP&countries=KR&countries=KW&countries=KZ&countries=LB&countries=LT&countries=LU&countries=LV&countries=MA&countries=MD&countries=ME&countries=MT&countries=MX&countries=MY&countries=MZ&countries=NG&countries=NL&countries=NO&countries=NZ&countries=OM&countries=PA&countries=PE&countries=PH&countries=PK&countries=PL&countries=PT&countries=PY&countries=QA&countries=RO&countries=RS&countries=RU&countries=SA&countries=SE&countries=SG&countries=SI&countries=SK&countries=TH&countries=TN&countries=TR&countries=TW&countries=UA&countries=UG&countries=US&countries=UY&countries=UZ&lastUpdated=ANYTIME&showOnlyNew=false&showOnlyResolved=false'

class Render(QWebPage):  
  def __init__(self, url):
    self.app = QApplication(sys.argv)         
         
    QWebPage.__init__(self)
    self.loadFinished.connect(self._loadFinished)  
    self.mainFrame().load(QUrl(url))  
    self.app.exec_()
  
  def _loadFinished(self, result):  
    self.frame = self.mainFrame()  
    self.app.quit()

def loadPage(url):
    page = QtWebKit.QWebPage()
    loop = QtCore.QEventLoop() # Create event loop
    page.mainFrame().loadFinished.connect(loop.quit) # Connect loadFinished to loop quit
    page.mainFrame().load(url)
    loop.exec_() # Run event loop, it will end on loadFinished
    return page.mainFrame().toHtml()

def retrive(url):
#    r = Render(url) 
#    page = r.frame.toHtml()
    page = loadPage(url)
    soup = BeautifulSoup(page, 'html.parser')
    
#    Table = soup.find('table', class_='ng-scope ng-table')
#    for T in Table.find_all('span', class_='ng-binding sort-indicator'):
#        print(T.text)
        # = []
    href = []
    TBody = soup.find('tbody')
    for T in TBody.find_all('a', class_='ng-binding'):
    #    print(T.text)
    #    print('https://madb.europa.eu/madb/'+T['href'])
        href.append('https://madb.europa.eu/madb/'+T['href'])
    return href
    #print('________________________________________________________________________')


#    for Tr in TBody.find_all('tr', class_='ng-scope'):
#        for T in Tr.find_all('td'):
#            #print(T['data-title-text'])
#            print(T.text)DictTable = {}
#        print('____________________________________')
    

    #for T in TBody.find_all('tr', class_='ng-scope'):
    #    print(T.text) ok
    

    #for T in TBody.find_all('td', data-title-text='Country'):
    #    print(T.text)

#def get_links(url):

def Repported_Barriers(url):
    page = loadPage(url)
    soup = BeautifulSoup(page, 'html.parser')
    TBody = soup.find('tbody')
    
    Barrier = dict()
    for Tr in TBody.find_all('tr'):
        T = Tr.find_all('td')
        Barrier[T[0].text] = T[1].text
    return Barrier
   
hrefs = []
Data = []

def Loadl_Pages():
    app = QtGui.QApplication(sys.argv)
    i = 0
    for url in urls:
        print('url',str(i))
        hrefs.extend(retrive(url))
        i+=1

#    pickle_in = open("hrefs.pkl","rb")
#    hrefs = pickle.load(pickle_in)
    
    for href in hrefs:
        Data.append(Repported_Barriers(href))

    app.exit()    
    
def Triggers():
    app = QtGui.QApplication(sys.argv)
    page = loadPage(urls[0])
    soup = BeautifulSoup(page, 'html.parser')
    pagelen = soup.find('ul', class_='tags ng-scope')
    print(pagelen['ng-if'])
    app.exit()    

def Click_Link():
    browser = webdriver.Chrome(executable_path=’/Library/Application Support/Google/chromedriver’, chrome_options=option)
    driver.find_element_by_css_selector("a[ng-switch-when='next']").click()
#Loadl_Pages()

#pickle_out = open("hrefs.pkl","wb")
#pickle.dump(hrefs, pickle_out)
#pickle_out.close()
#
#pickle_out = open("RepportedBarriers.pkl","wb")
#pickle.dump(Data, pickle_out)
#pickle_out.close()  
#
#with open('RepportedBarriers.csv', 'w', encoding='utf8', newline='') as output_file:
#     fc = csv.DictWriter(output_file, fieldnames=Data[0].keys())
#     fc.writeheader()
#     fc.writerows(Data)