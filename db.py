#https://www.youtube.com/watch?v=fM_Os976HsQ
from sqlite3 import Cursor
import pyodbc,requests,configparser,os,sys,json
from bs4 import BeautifulSoup
from requests.auth import HTTPProxyAuth
from time import sleep

# Set path from other file
def set_path(path,config):
  global path_config
  global config_file
  path_config=path
  config_file=config


#query='SELECT distinct [MANI_BUQUE] from dbo.TBL_MANIFIESTOS ORDER BY MANI_BUQUE'
query = 'SELECT distinct [MANI_BUQUE] from dbo.TBL_BUQUES_MARINE_TRAFFIC mb left join dbo.TBL_BUQUES b on b.NOMBRE = mb.MANI_BUQUE where b.NOMBRE is null ORDER BY MANI_BUQUE;'
config = configparser.ConfigParser()
config.read(os.path.dirname(os.path.realpath(__file__))+'\\buques.ini') #SAME DIR
base = config['CONFIG']['base_server']
#print("conexion realizada")

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

#Run procedure generic
def run_proc(proc,data=()):
		config = configparser.ConfigParser()
		config.read(path_config + '\\' + config_file)
		base=config['CONFIG']['base_server']
		db=config['CONFIG']['base_db']
		usr=config['CONFIG']['base_usr']
		pwd=config['CONFIG']['base_pass']
		cnxn = pyodbc.connect("Driver={ODBC Driver 11 for SQL Server};"
						 +"Server="+base+
						"Database="+db+
						"UID="+usr+
						"PWD="+pwd
						)
		cursor = cnxn.cursor()
		if len(data) > 0:
				sql = '{call'+ proc + '('
				for i in data:
					sql = sql + '?,'
				sql =(sql + ')}').replace(',)}',')}')
				print(sql)
				cnxn.execute(slq,data)
		else:
				print('no params')
				sql = '{call' + proc +'}'
				cnxn.execute(sql)
				cnxn.commit()
				cnxn.close()

						