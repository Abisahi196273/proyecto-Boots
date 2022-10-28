import requests,sys,html,datetime,os,re,time,json,pywinauto,configparser,logging,threading,zipfile,shutil
import pyodbc

from bs4 import BeautifulSoup
from time import sleep
from pywinauto.findwindows import find_window
from pywinauto.application import Application
from collections import OrderedDict
from logging import Logger

import sys
sys.path.insert(0, 'C:/Domain_User/')
from gets_constants import (get_user_pass)

data_login = get_user_pass() 
# Function to create, if not exists, a 
#file_path = 'C:/Manifiestos/buques'
def create_dir(file_path):
    directory = os.path.dirname(file_path)
    try:
            os.makedirs(directory)
    except:
            print(directory)
            pass

# Get all inputs on a <tag> filetype (xml,html,krt,kjb,etc)
def get_data(btfsoup):
    d=dict()
    params = list(btfsoup.find_all(['input']))
    for x in params:
        if x.get('value') is None:
            d[x.get('name')]=''
        else:
            d[x.get('name')]=x.get('value')
    return d

# Function to repair kilo error in a file
def remplace_kilo_error(txt):
    regex_kilo='^(((?!\|).)*\|){2}KILO'
    regex_peso=r'([0-9]+\.[0-9]{2}\|)'
    filter_kilo=re.compile(regex_kilo,re.MULTILINE|re.DOTALL)
    for i in filter_kilo.finditer(txt):
        normal=i.group(0)
        replaced=re.sub(regex_peso,r'\1\1',i.group(0))
        txt=txt.replace(normal,replaced)
    return txt

# Change path type / per \
def parse_path(path):
    return path.replace('/','\\')#remplace el Dir
# If null return empty
def none(string):
    if string is None:
        return ''
    else:
        return string.strip()

# Return all array as string
def data_as_string(data):
    result=''
    for i in data:
        result=result +'"' + i + '"'
    return result

def zipdir(path,name):
    ziph=zipfile.ZipFile(name+'.zip', 'w', zipfile.ZIP_DEFLATED)
    for root, dirs, files in os.walk(path):
        for file in files:
            ziph.write(os.path.join(root, file),os.path.basename(file))
    ziph.close()
    #shutil.rmtree(
# Change path type / per \
def parse_path(path):
    return path.replace('/','\\')#remplace el Dir
# If null return empty
def none(string):
    if string is None:
        return ''
    else:
        return string.strip()

