from urllib.request import urlopen
from bs4 import BeautifulSoup, Comment

import csv
import xml
import pickle
import requests

from selenium.webdriver.firefox.options import Options


from selenium import webdriver
from selenium.common.exceptions import TimeoutException, NoSuchElementException
from selenium.webdriver.common.by import By
from selenium.webdriver.support.ui import WebDriverWait
from selenium.webdriver.support import expected_conditions as EC

ASps = 'https://madb.europa.eu/madb/sps_barriers_result.htm?isSps=true&sectors=5&sectors=6&sectors=7&sectors=8&sectors=9&sectors=10&sectors=11&sectors=12&sectors=13&sectors=14&sectors=15&sectors=16&sectors=17&sectors=18&sectors=19&sectors=20&sectors=32&sectors=21&sectors=22&sectors=33&sectors=23&sectors=24&sectors=25&sectors=26&sectors=27&sectors=28&sectors=29&sectors=30&sectors=1&sectors=2&sectors=3&sectors=4&measures=43&measures=44&measures=45&measures=46&measures=47&measures=48&measures=49&measures=50&measures=51&measures=52&measures=53&measures=54&measures=55&measures=56&measures=57&measures=58&measures=59&measures=60&measures=61&measures=62&measures=63&measures=64&measures=65&measures=66&measures=67&measures=68&measures=69&measures=70&measures=71&measures=72&measures=73&measures=74&measures=75&measures=76&measures=77&measures=78&measures=79&measures=80&measures=81&measures=82&measures=83&measures=84&measures=85&measures=86&measures=87&measures=88&countries=AD&countries=AE&countries=AF&countries=AM&countries=AO&countries=AR&countries=AT&countries=AU&countries=BA&countries=BD&countries=BE&countries=BG&countries=BO&countries=BR&countries=BW&countries=BY&countries=CA&countries=CH&countries=CL&countries=CM&countries=CN&countries=CO&countries=CY&countries=CZ&countries=DE&countries=DK&countries=DO&countries=DZ&countries=EC&countries=EE&countries=EG&countries=ES&countries=FI&countries=FR&countries=GB&countries=GR&countries=HK&countries=HR&countries=HU&countries=ID&countries=IE&countries=IL&countries=IN&countries=IQ&countries=IR&countries=IS&countries=IT&countries=JO&countries=JP&countries=KR&countries=KW&countries=KZ&countries=LB&countries=LT&countries=LU&countries=LV&countries=MA&countries=MD&countries=ME&countries=MT&countries=MX&countries=MY&countries=MZ&countries=NG&countries=NL&countries=NO&countries=NZ&countries=OM&countries=PA&countries=PE&countries=PH&countries=PK&countries=PL&countries=PT&countries=PY&countries=QA&countries=RO&countries=RS&countries=RU&countries=SA&countries=SE&countries=SG&countries=SI&countries=SK&countries=TH&countries=TN&countries=TR&countries=TW&countries=UA&countries=UG&countries=US&countries=UY&countries=UZ&countries=VE&countries=VN&countries=ZA&lastUpdated=ANYTIME&showOnlyNew=false&showOnlyResolved=false'
NAAps = 'https://madb.europa.eu/madb/barriers_result.htm?isSps=&sectors=5&sectors=6&sectors=7&sectors=8&sectors=9&sectors=10&sectors=11&sectors=12&sectors=13&sectors=14&sectors=15&sectors=16&sectors=17&sectors=18&sectors=19&sectors=20&sectors=32&sectors=21&sectors=22&sectors=33&sectors=23&sectors=24&sectors=25&sectors=26&sectors=27&sectors=28&sectors=29&sectors=30&sectors=1&sectors=2&sectors=3&measures=100&measures=101&measures=102&measures=103&measures=104&measures=105&measures=106&measures=107&measures=108&measures=109&measures=110&measures=111&measures=112&measures=113&measures=114&measures=115&measures=116&measures=117&measures=118&measures=119&measures=120&measures=121&measures=164&measures=43&measures=44&measures=45&measures=46&measures=47&measures=48&measures=49&measures=50&measures=51&measures=52&measures=53&measures=54&measures=55&measures=56&measures=57&measures=58&measures=59&measures=60&measures=61&measures=62&measures=63&measures=64&measures=65&measures=66&measures=67&measures=68&measures=69&measures=70&measures=71&measures=72&measures=73&measures=74&measures=75&measures=76&measures=77&measures=78&measures=79&measures=80&measures=81&measures=82&measures=83&measures=84&countries=AD&countries=AE&countries=AF&countries=AM&countries=AO&countries=AR&countries=AT&countries=AU&countries=BA&countries=BD&countries=BE&countries=BG&countries=BO&countries=BR&countries=BW&countries=BY&countries=CA&countries=CH&countries=CL&countries=CM&countries=CN&countries=CO&countries=CY&countries=CZ&countries=DE&countries=DK&countries=DO&countries=DZ&countries=EC&countries=EE&countries=EG&countries=ES&countries=FI&countries=FR&countries=GB&countries=GR&countries=HK&countries=HR&countries=HU&countries=ID&countries=IE&countries=IL&countries=IN&countries=IQ&countries=IR&countries=IS&countries=IT&countries=JO&countries=JP&countries=KR&countries=KW&countries=KZ&countries=LB&countries=LT&countries=LU&countries=LV&countries=MA&countries=MD&countries=ME&countries=MT&countries=MX&countries=MY&countries=MZ&countries=NG&countries=NL&countries=NO&countries=NZ&countries=OM&countries=PA&countries=PE&countries=PH&countries=PK&countries=PL&countries=PT&countries=PY&countries=QA&countries=RO&countries=RS&countries=RU&countries=SA&countries=SE&countries=SG&countries=SI&countries=SK&countries=TH&countries=TN&countries=TR&countries=TW&countries=UA&countries=UG&countries=US&countries=UY&countries=UZ&countries=VE&countries=VN&countries=ZA&lastUpdated=ANYTIME&showOnlyNew=false&showOnlyResolved=false'

ActiveSps = 'https://webgate.ec.europa.eu//barriers/public/v1/barriers?isSps=true&country=AD&country=AE&country=AF&country=AM&country=AO&country=AR&country=AT&country=AU&country=BA&country=BD&country=BE&country=BG&country=BO&country=BR&country=BW&country=BY&country=CA&country=CH&country=CL&country=CM&country=CN&country=CO&country=CY&country=CZ&country=DE&country=DK&country=DO&country=DZ&country=EC&country=EE&country=EG&country=ES&country=FI&country=FR&country=GB&country=GR&country=HK&country=HR&country=HU&country=ID&country=IE&country=IL&country=IN&country=IQ&country=IR&country=IS&country=IT&country=JO&country=JP&country=KR&country=KW&country=KZ&country=LB&country=LT&country=LU&country=LV&country=MA&country=MD&country=ME&country=MT&country=MX&country=MY&country=MZ&country=NG&country=NL&country=NO&country=NZ&country=OM&country=PA&country=PE&country=PH&country=PK&country=PL&country=PT&country=PY&country=QA&country=RO&country=RS&country=RU&country=SA&country=SE&country=SG&country=SI&country=SK&country=TH&country=TN&country=TR&country=TW&country=UA&country=UG&country=US&country=UY&country=UZ&country=VE&country=VN&country=ZA&sectorId=5&sectorId=6&sectorId=7&sectorId=8&sectorId=9&sectorId=10&sectorId=11&sectorId=12&sectorId=13&sectorId=14&sectorId=15&sectorId=16&sectorId=17&sectorId=18&sectorId=19&sectorId=20&sectorId=32&sectorId=21&sectorId=22&sectorId=33&sectorId=23&sectorId=24&sectorId=25&sectorId=26&sectorId=27&sectorId=28&sectorId=29&sectorId=30&sectorId=1&sectorId=2&sectorId=3&sectorId=4&measureId=43&measureId=44&measureId=45&measureId=46&measureId=47&measureId=48&measureId=49&measureId=50&measureId=51&measureId=52&measureId=53&measureId=54&measureId=55&measureId=56&measureId=57&measureId=58&measureId=59&measureId=60&measureId=61&measureId=62&measureId=63&measureId=64&measureId=65&measureId=66&measureId=67&measureId=68&measureId=69&measureId=70&measureId=71&measureId=72&measureId=73&measureId=74&measureId=75&measureId=76&measureId=77&measureId=78&measureId=79&measureId=80&measureId=81&measureId=82&measureId=83&measureId=84&measureId=85&measureId=86&measureId=87&measureId=88&lastUpdated=ANYTIME&showOnlyNew=false&showOnlyResolved=false'
NonActiveSps = 'https://webgate.ec.europa.eu//barriers/public/v1/barriers?isSps=&country=AD&country=AE&country=AF&country=AM&country=AO&country=AR&country=AT&country=AU&country=BA&country=BD&country=BE&country=BG&country=BO&country=BR&country=BW&country=BY&country=CA&country=CH&country=CL&country=CM&country=CN&country=CO&country=CY&country=CZ&country=DE&country=DK&country=DO&country=DZ&country=EC&country=EE&country=EG&country=ES&country=FI&country=FR&country=GB&country=GR&country=HK&country=HR&country=HU&country=ID&country=IE&country=IL&country=IN&country=IQ&country=IR&country=IS&country=IT&country=JO&country=JP&country=KR&country=KW&country=KZ&country=LB&country=LT&country=LU&country=LV&country=MA&country=MD&country=ME&country=MT&country=MX&country=MY&country=MZ&country=NG&country=NL&country=NO&country=NZ&country=OM&country=PA&country=PE&country=PH&country=PK&country=PL&country=PT&country=PY&country=QA&country=RO&country=RS&country=RU&country=SA&country=SE&country=SG&country=SI&country=SK&country=TH&country=TN&country=TR&country=TW&country=UA&country=UG&country=US&country=UY&country=UZ&country=VE&country=VN&country=ZA&sectorId=5&sectorId=6&sectorId=7&sectorId=8&sectorId=9&sectorId=10&sectorId=11&sectorId=12&sectorId=13&sectorId=14&sectorId=15&sectorId=16&sectorId=17&sectorId=18&sectorId=19&sectorId=20&sectorId=32&sectorId=21&sectorId=22&sectorId=33&sectorId=23&sectorId=24&sectorId=25&sectorId=26&sectorId=27&sectorId=28&sectorId=29&sectorId=30&sectorId=1&sectorId=2&sectorId=3&measureId=100&measureId=101&measureId=102&measureId=103&measureId=104&measureId=105&measureId=106&measureId=107&measureId=108&measureId=109&measureId=110&measureId=111&measureId=112&measureId=113&measureId=114&measureId=115&measureId=116&measureId=117&measureId=118&measureId=119&measureId=120&measureId=121&measureId=164&measureId=43&measureId=44&measureId=45&measureId=46&measureId=47&measureId=48&measureId=49&measureId=50&measureId=51&measureId=52&measureId=53&measureId=54&measureId=55&measureId=56&measureId=57&measureId=58&measureId=59&measureId=60&measureId=61&measureId=62&measureId=63&measureId=64&measureId=65&measureId=66&measureId=67&measureId=68&measureId=69&measureId=70&measureId=71&measureId=72&measureId=73&measureId=74&measureId=75&measureId=76&measureId=77&measureId=78&measureId=79&measureId=80&measureId=81&measureId=82&measureId=83&measureId=84&lastUpdated=ANYTIME&showOnlyNew=false&showOnlyResolved=false'

columns = ['barrierId','barrierResolved','barrierStatus','country','description','keyBarrier',
           'reportedDate','lastUpdateDate','sps','title','measures','products','sectors']

link = 'https://madb.europa.eu/madb/'
def getPages():
#    over=urlopen(link).read()
#    soup = BeautifulSoup(over, features="lxml")
#    Pages = soup.find('span',attrs={"class":"pagebanner ng-binding"})
#    return Pages
    response = requests.get(link)
    soup = BeautifulSoup(response.text, 'html.parser')
    #soup.findAll('span',attrs={"class":"pagebanner ng-binding"})
    #results = soup.find('span',attrs={"class":'pagebanner ng-binding'})
    
    soup = soup.find(id='col-2')
    print(soup)
    
    results = []
    
    li_list = soup.findAll('li')
    for li in li_list:
        print(li)
        print('________________________________________________________________')
#        if li['ng-repeat'] == 'page in pages':
#           results.append(li.text)
           
    print(results)

def Scraper():
    driver = webdriver.Firefox(executable_path = '/home/polo/.config/spyder-py3/Barriers Identification/Barriers DashBoard/Scraping MADB/geckodriver')
    driver.get(link)
    print (driver.title)
   
    print (driver.FindElement(By.tagName("body")).getText())
    items = driver.find_elements_by_class_name("main")

    time.sleep(5)
    driver.quit()
    return items

def ScraperJS():
    driver = webdriver.PhantomJS(executable_path = '/home/polo/.config/spyder-py3/Barriers Identification/Barriers DashBoard/Scraping MADB/geckodriver')
    driver.get(link)
    print (driver.title)
    html = driver.execute_script()
    items = html.find_element_by_css_selector("a[ng-switch-when='page']")#.click()
    print(items)
    time.sleep(5)
    driver.quit()
    return items

def ActiveSPSMADB(Sps = True):
    data =[]
    if Sps:
       for i in range (1,12):
           r = requests.get(ActiveSps+'&page='+str(i)+'&pageSize=10')
           data.append(r.json())
    else:
       for i in range (1,43):
           r = requests.get(NonActiveSps+'&page='+str(i)+'&pageSize=10')
           data.append(r.json())
       
    return data

def MADB_to_CSV(pages,name):
    
    data_list = [columns]
    for page in pages:
        for Barrier in page['publicBarriers']:
            data = []
            for column in columns:
#                data.append(Barrier[column])
                if column == 'description':
                   data.append(BeautifulSoup(Barrier[column], "lxml").text)
                else:
                    data.append(Barrier[column])
            data_list.append(data)

    with open(name+'.csv', 'w', newline='') as file:
         writer = csv.writer(file, delimiter='\t')
         writer.writerows(data_list)

#ActiveSpsData =  ActiveSPSMADB(Sps = True)
#pickle_out = open("MADB/ActiveSpsData.pkl","wb")
#pickle.dump(ActiveSpsData, pickle_out)
#pickle_out.close()
#
#NonActiveSpsData =  ActiveSPSMADB(Sps = False)
#pickle_out = open("MADB/NonActiveSpsData.pkl","wb")
#pickle.dump(NonActiveSpsData, pickle_out)
#pickle_out.close()         

pickle_in = open("MADB/ActiveSpsData.pkl","rb")
ActiveSpsData = pickle.load(pickle_in)
#MADB_to_CSV(ActiveSpsData,'MADB/ActiveSpsData')

pickle_in = open("MADB/NonActiveSpsData.pkl","rb")
NonActiveSpsData = pickle.load(pickle_in)
#MADB_to_CSV(NonActiveSpsData,'MADB/NonActiveSpsData')