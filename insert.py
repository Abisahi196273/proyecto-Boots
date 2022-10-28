import pyodbc,configparser,shutil,zipfile,datetime,logging
import json
import os
import sys
from collections import OrderedDict
from func import (create_dir)

path_config=''
config_file=''  

# Set path from other file
def set_path(path,config):
  global path_config
  global config_file
  path_config=path
 
# Get list of json files
def get_files(folder):
    #folder='C:/Manifiestos/Per_Mani'
    list_files=list()
    for file in os.listdir(folder):
        if file.endswith('.json'):
            list_files.append(os.path.join(folder,file))
    return list_files


# To insert json file
def insert_json(file,logger):
    json_data=open(file,encoding='utf-8').read()
    data = json.loads(json_data,object_pairs_hook=OrderedDict)
    print("enviar data")