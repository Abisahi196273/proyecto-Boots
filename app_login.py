#https://www.youtube.com/watch?v=ZE5hXt-tFiM
#https://www.autoscripts.net/raise-timeoutexceptionmessage-screen-stacktrace-timeoutexception-message/
#imports here
from cgi import print_form
from distutils.log import info
from itertools import count
from lib2to3.pgen2 import driver
from posixpath import split
from re import search
from turtle import title
from unicodedata import name
from unittest import result
from selenium import webdriver
import requests
from random_user_agent.params import SoftwareName, OperatingSystem
from bs4 import BeautifulSoup
from selenium.webdriver.common.keys import Keys
from selenium.webdriver.support import expected_conditions as EC
from selenium.webdriver.common.by import By
from selenium.webdriver.support.wait import WebDriverWait
from selenium.webdriver.chrome.options import Options
from selenium.webdriver.support.ui import WebDriverWait
from selenium.webdriver.support.ui import Select
from selenium.webdriver.common.desired_capabilities import DesiredCapabilities
from requests.auth import HTTPProxyAuth
import unittest
from selenium.webdriver.chrome.service import Service
from webdriver_manager.chrome import ChromeDriverManager
import random
import time
import lxml as html
import pyodbc,requests,configparser,os,sys,json
from bs4 import BeautifulSoup
from requests.auth import HTTPProxyAuth
#from time import sleep

#se define la url a consultar
BASE_URL='https://www.marinetraffic.com'
SEARCH_URL=BASE_URL + '/en/ais/index/search/all'
headers={'User-Agent':'Mozilla/5.0 (Windows NT 6.1; WOW64; rv:40.0) Gecko/20100101 Firefox/40.1'}

driver_service = Service(executable_path="D:/CURSO_PYTHON_NIVEL_ONE/chromedriver.exe")
driver = webdriver.Chrome()
driver.maximize_window()
driver.get(SEARCH_URL)

#definir perfil
emailFieldId = "abisa_hi91@hotmail.com"
passFieldId = "Leslie2590"

#Cdo para habilita pagina de desbloqueo 
egree_data = WebDriverWait(driver,10).until(EC.element_to_be_clickable((By.CSS_SELECTOR, "button[mode='primary']"))).click()
	
#Exe botono de login para abrir interfaz de login para validar credencial
log_ing = WebDriverWait(driver,10).until(EC.element_to_be_clickable((By.XPATH, '/html/body/header/div[2]/header/div/div/div[6]/div/div[2]/button'))).click()

#target username
emailFieldElement = WebDriverWait(driver, 20).until(EC.element_to_be_clickable((By.CSS_SELECTOR, "input[name='email']")))
passFieldElement = WebDriverWait(driver, 20).until(EC.element_to_be_clickable((By.CSS_SELECTOR, "input[id='password']")))
#enter username and password
emailFieldElement.clear()
emailFieldElement.send_keys(str(emailFieldId))
passFieldElement.clear()
passFieldElement.send_keys(str(passFieldId))
#lon_inButtonElement = WebDriverWait(driver, 10).until(EC.element_to_be_clickable((By.CSS_SELECTOR, "button[id='#login_form_submit']"))).click()
LOGIN = WebDriverWait(driver, 10).until(EC.element_to_be_clickable((By.XPATH, '//*[@id="login_form_submit"]'))).click()
time.sleep(100)

#designacion de Proxies
PROXIES = { 'http' : 'proxy.sat.gob.mx:3128',
            'https' : 'proxy.sat.gob.mx:3128'}
AUTH = HTTPProxyAuth('gamd786b', 'Veracruz.2025')
#se define la url a consultar
BASE_URL='https://www.marinetraffic.com'
SEARCH_URL=BASE_URL + '/en/ais/index/search/all'
headers={'User-Agent':'Mozilla/5.0 (Windows NT 6.1; WOW64; rv:40.0) Gecko/20100101 Firefox/40.1'}

query = 'SELECT distinct [MANI_BUQUE] from dbo.TBL_BUQUES_MARINE_TRAFFIC'
config = configparser.ConfigParser()
config.read(os.path.dirname(os.path.realpath(__file__))+'\\buques.ini') #SAME DIR
base = config['CONFIG']['base_server']
print("conexion realizada")

def run_query(query):
	cnxn = pyodbc.connect("Driver={ODBC Driver 11 for SQL Server};"
                      +"Server="+base+
                      "Database=buques;"
                      "UID=sa;"
                      "PWD=Oaxaca.2022$"
                      )
	cursor = cnxn.cursor()
	data=[]
	try:
		cursor.execute(query)
		for row in cursor:
			data.append(row[0])
		cnxn.close()
	except:
		print("esta vacia")
		raise
	return data

def insert_data(data):
	cnxn = pyodbc.connect("Driver={ODBC Driver 11 for SQL Server};"
                      +"Server="+base+
                      "Database=buques;"
                      "UID=sa;"
                      "PWD=Oaxaca.2022$"
                      )
	cursor = cnxn.cursor()
	query = 'INSERT INTO [buques].[dbo].[TBL_BUQUES] (IMO, NOMBRE, OLD_NOMBRE, TIPO,USUARIO,FEC_CARGA,BSTATUS)VALUES (?,?,?,?,1,GETDATE(),1);'
	cursor.execute(query,data)
	cnxn.commit()
	cnxn.close()

#Definimos los parametros de Session
MAX_RETRIES=1 # Reintentos
session=requests.Session() 
adapter = requests.adapters.HTTPAdapter(max_retries=MAX_RETRIES)
session.mount('https://', adapter)
session.mount('http://', adapter)

# Se realiza la peticion con los parametros y valores asignado
buques=list()
data=dict()
data['keyword']=''
result = run_query(query)
for r in result:
        print(r)
        data['keyword'] = r.strip()
        page=session.get(SEARCH_URL,params = data,headers=headers,proxies=PROXIES,auth=AUTH)
        #print(page.text)
        soup_i=BeautifulSoup(page.text, 'lxml')
        All_names=((soup_i.find('table', {'class':'table table-hover text-left'})).find_all('tr'))
        index=1
        #print(All_names)
        try:
            while index < len(All_names):
                print(index)
                if (All_names[index].find_all('td')[1] != 'Photographer' or All_names[index].find_all('td')[1] !='Light'):
                    #print(BASE_URL + All_names[index].find_all('td')[0].find('a').get('href'))
                    np = session.get(BASE_URL + All_names[index].find_all('td')[0].find('a').get('href'),headers=headers,proxies=PROXIES,auth=AUTH)
                    soup =BeautifulSoup(np.text,'lxml')
                    
                    imo = soup.find('div',{'class':'group-ib short-line'}.find('p').string())
                    #print(imo.prettify).text
                    other_info =soup.find('title').string.split(':')[1].split(',')[0].split()
                    title = other_info.split('-')
            

                    count = 0
                    name = r
                    new_name = ''
                    tipo = ''
                    imo = ''
                    while count < (title):
                        if count == 0:
                            tmp_data = title[count].split('(')
                            new_name = tmp_data[0].split()
                            tipo = tmp_data[1].replace(')','').strip()
                            if count ==1:
                                imo = title[count].replace('IMO','').strip()
                                count+=1
                                
                                insert_data([imo,name,new_name,tipo])
                                buques.append({'imo':imo,'name':name,'new_name':new_name,'tipo':tipo})
                                index+=1


                    other_info=soup.find_all('li',{'class':'group-ib medium-gap line-120 vertical-offset-10'})
				#print(soup_i.find('title'))
                for info in other_info:
                    
                    field=info.find('span',text=True, recursive=False)
                    print(field)
                    value=info.find('span').find('b').string
                    print(value)
        except:
                print("")
"""                    
                    #sleep(90)
                    
                    imo=soup.find('div',{'class':'group-ib short-line'}).find('b').string.strip()
                    status = ''
                    tipo = ''
                    for j in soup.find_all('div',{'class':'group-ib short-line vertical-offset-5'}):
                        field = j.find('span').string.strip().replace(':','')
                        value = j.find('b').string.strip()
                        if field == "Status":
                            status = value
                        elif field == "AIS Vessel Type":
                            tipo = value
                        
                    insert_data([imo,name,new_name,tipo])		
                    buques.append({'imo':imo,'name':name,'new_name':new_name,'tipo':tipo})
                index+=1           
        except Exception as e:
                insert_data([' No imo',r,r,'Container Ship'])
                buques.append({'imo':imo,'name':name,'new_name':new_name,'tipo':tipo})
                print(e,"no se encontro datos")

for buque in buques:
    print(buque)
"""
