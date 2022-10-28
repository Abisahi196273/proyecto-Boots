from cgi import print_form
from concurrent.futures import thread
from distutils.command.config import config
from distutils.log import info
from itertools import count
from lib2to3.pgen2 import driver
from pathlib import Path
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
import requests, sys, datetime, os, re, configparser, logging, threading, shutil, traceback,json
from random_user_agent.user_agent import UserAgent
from random_user_agent.params import SoftwareName, OperatingSystem
from dateutil.relativedelta import relativedelta
import urllib3
import lxml as html
from db import set_path, run_proc
from func import create_dir,zipdir,parse_path
from  insert import get_files,insert_json

sys.path.insert(0, 'C:/Domain_User/')
from gets_constants import (get_user_pass)
data_login = get_user_pass()


today = datetime.datetime.today()  # HOY
exe = ''
folder = ''
folder_fecha = ''
log_append = ''
any_fails = False

path_config = str(os.path.dirname(os.path.realpath(__file__)))
config_file = 'config_mai.ini'
list_eta = []
set_path(path_config, config_file)

try:
    fecha = (datetime.datetime.strptime(sys.argv[1], '%d-%m-%Y')).strftime('%d-%m-%Y')
except IndexError:
    #print('No se recibio parametro de fecha, se tomará la actual')
    fecha = (today).strftime('%d-%m-%Y')
print(fecha)
hora = datetime.datetime.now().strftime("%H:%M:%S")
log_append = datetime.datetime.now().strftime("%Y%m%d %H:%M")
print(log_append)
class CustomError(Exception):
    pass

def scraping(offset, rows_query):
    global path_config
    global exe
    global folder
    global folder_fecha
    global log_append
    global hora
    global today
    global date_min
    global date_max
    global eta_min
    global eta_max

    config = configparser.ConfigParser()
    config.read(path_config + '\\' + config_file)  # SAME DIR
    root = config['CONFIG']['root']
    
    threads_list=[]
    #SE CREA UN DICCIONARIO PARA VALIDAR
    valid_1 = 'NO HAY ETA.'
    list_manifiestos = ['']
    success = False

    if_error=False
    regex_kilo = '^(((?!\|).)*\|){2}KILO'
    delay_attemps = 10
    max_attemps = 100
    attemp = 1

    #SE CREAN LAS CARPETAS DE LA CUAL SE VAN  GUARDAR  REGISTRO
    folder_fecha = root + datetime.datetime.strptime(fecha,'%d-%m-%Y').strftime('%Y%m%d')+"/"
    ini = (today + relativedelta(days=+(date_min))).strftime('%d-%m-%Y')
    fin = (today + relativedelta(days=+(date_max))).strftime('%d-%m-%Y')
    eta_ini = today + relativedelta(days=+(eta_min))
    eta_fin = today + relativedelta(days=+(eta_max))
    print(ini, fin)
    print(eta_ini, eta_fin)
    folder = folder_fecha + hora
    print(folder_fecha)
#SE CREA UN LOGER PARA ESCRIBIR REGISTROS EN UN ARCHIVO
    logger = logging.getLogger(__name__ + 'thread' + str(offset))
    logger.setLevel(logging.DEBUG)
    ch = logging.StreamHandler()
    ch.setLevel(logging.DEBUG)
    formatter = logging.Formatter('%(asctime)s - %(levelname)s - %(message)s')
    ch.setFormatter(formatter)
    logger.addHandler(ch)
    print(logger)
#SE CREA LA CARPETA DE DESCARGA
    print(create_dir(folder_fecha))
    fh = logging.FileHandler(r'' + folder_fecha + log_append + "_message_" + str(offset) + ".log")
    fh.setFormatter(formatter)
    logger.addHandler(fh)

    logger.info("Descargando " + fecha + '|hilo ' + str(offset))
    
    
#se define la url a consultar
BASE_URL='https://www.marinetraffic.com'
SEARCH_URL=BASE_URL + '/en/ais/index/search/all'         #'/en/ais/index/search/all'
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
time.sleep(50)

#designacion de Proxies
PROXIES = { 'http' : 'proxy.sat.gob.mx:3128',
            'https' : 'proxy.sat.gob.mx:3128'}
AUTH = HTTPProxyAuth('gamd786b', 'Veracruz.2025')
#se define la url a consultar
BASE_URL='https://www.marinetraffic.com/'
SEARCH_URL=BASE_URL + 'en/ais/index/search/all'
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
#query = 'truncate table TBL_BUQUES'
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
        #soup_i=BeautifulSoup(page.text, 'lxml')
        soup_i = BeautifulSoup(driver.page_source,'lxml')
        #print(soup_i.title.text)
        All_names=((soup_i.find('table', {'class':'table table-hover text-left'})).find_all('tr'))
        index=1
        #print(All_names)
        try:
                while index < len(All_names):
                    #print(index)
                    if (All_names[index].find_all('td')[1] != 'Photographer' or All_names[index].find_all('td')[1] !='Light'):
                        #print(BASE_URL + All_names[index].find_all('td')[0].find('a').get('href'))
                        eta = session.get(SEARCH_URL + All_names[index].find_all('tr')[0].find('a').get('href'),headers=headers,proxies=PROXIES,auth=AUTH)
                        soup =BeautifulSoup(eta.text,'lxml')
                        imo = soup.find('div',{'class':'group-ib short-line'}).find('b').string.strip()
                        print(imo.prettify).text

                        other_info =soup.find('title').string.split(':')[1].split(',')[0].split()
                        title = other_info.split('-')
                        
                        count = 0
                        name = r
                        new_name = ''
                        tipo = ''
                        imo = ''
                        while count < len(title):
                            if count == 0:
                                tmp_data = title[count].split('(')
                                new_name = tmp_data[0].split()
                                tipo = tmp_data[1].replace(')','').strip()
                            if count ==1:
                                    imo = title[count].replace('Imo','').strip()
                            count+=1
            
                for info in other_info:
                        field=info.find('span',text=True, recursive=False)
                        value=info.find('span').find('b').string
                        #print(value)
                imo = soup.find('div',{'class':'group-ib short-line'}).find('b').string.strip()
                status  =''
                tipo = ''
                for j in soup.find_all('div',{'class':'group-ib short-line vertical-offset-5'}):   
                        field = j.find('span').string.strip().replace('','+')
                        value = j.find('b').string.strip()
                        if field == "status":
                                status = value
                        elif field == "AIS Vessel Type":
                                tipo = value   


                insert_data([imo,name,new_name,tipo])
                print(buques.append({'imo':imo,'name':name,'new_name':new_name,'tipo':tipo})).text
                index+=1

        except Exception as e:
                insert_data(['No imo',r,r,'Container Ship'])
                print(buques.append({'imo':'No imo','name':name,'new_name':name,'tipo':'Container Ship'})) + "//r"
                index+=1
                print(e, "Data not found")
                continue   

for buque in buques:
    print(buque)
driver.close()
