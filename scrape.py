import pyodbc,requests,configparser,os,sys,json
from bs4 import BeautifulSoup
from requests.auth import HTTPProxyAuth
from time import sleep


PROXIES = { 'http' : 'proxy.sat.gob.mx:3128',
            'https' : 'proxy.sat.gob.mx:3128'}
AUTH = HTTPProxyAuth('HEAY928M', 'Nalle1408*')

BASE_URL='https://www.marinetraffic.com'
SEARCH_URL=BASE_URL + '/en/ais/index/search/all'
headers={'User-Agent':'Mozilla/5.0 (Windows NT 6.1; WOW64; rv:40.0) Gecko/20100101 Firefox/40.1'}


#query='SELECT distinct [MANI_BUQUE] from dbo.TBL_MANIFIESTOS ORDER BY MANI_BUQUE'
query = 'SELECT distinct [MANI_BUQUE] from dbo.TBL_MANIFIESTOS mb left join dbo.TBL_BUQUES b on b.NOMBRE = mb.MANI_BUQUE where b.NOMBRE is null ORDER BY MANI_BUQUE;'
config = configparser.ConfigParser()
config.read(os.path.dirname(os.path.realpath(__file__))+'\\config.ini') #SAME DIR
base=config['CONFIG']['base_server']

def run_query(query):
	cnxn = pyodbc.connect("Driver={ODBC Driver 11 for SQL Server};"
                      +"Server="+base+
                      "Database=ANALISIS;"
                      "UID=sa;"
                      "PWD=Mr7895123"
                      )
	cursor = cnxn.cursor()
	cursor.execute(query)
	data=[]
	for row in cursor:
		data.append(row[0])
	cnxn.close()
	return data

def insert_data(data):
	cnxn = pyodbc.connect("Driver={ODBC Driver 11 for SQL Server};"
                      +"Server="+base+
                      "Database=ANALISIS;"
                      "UID=sa;"
                      "PWD=Mr7895123"
                      )
	cursor = cnxn.cursor()
	query = 'INSERT INTO [ANALISIS].[dbo].[TBL_BUQUES] (IMO, NOMBRE, OLD_NOMBRE, TIPO,USUARIO,FEC_CARGA,BSTATUS)VALUES (?,?,?,?,1,GETDATE(),1);'
	cursor.execute(query,data)
	cnxn.commit()
	cnxn.close()

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
	data['keyword']=r.strip()
	page=session.get(SEARCH_URL,params = data,headers=headers,proxies=PROXIES,auth=AUTH)
	print(page.text)
	soup_i=BeautifulSoup(page.text, 'lxml')
	All_names=((soup_i.find('table',{'class':'table table-hover text-left'})).find_all('tr'))
	index=1
	try:
		while index < len(All_names):
			print(index)
			if (All_names[index].find_all('td')[1] != 'Photographer' or All_names[index].find_all('td')[1] != 'Light'): #and All_names[index].find_all('td')[0].find('a').string.strip() == r.strip():
				print(BASE_URL + All_names[index].find_all('td')[0].find('a').get('href'))
				np=session.get(BASE_URL + All_names[index].find_all('td')[0].find('a').get('href'),headers=headers,proxies=PROXIES,auth=AUTH)
				soup=BeautifulSoup(np.text, 'lxml')
				print(np.text)
				imo=soup.find('div',{'class':'group-ib short-line'}).find('b').string.strip()
				other_info=soup.find('title').string.split(':')[1].split(',')[0].strip()
				title=other_info.split('-')
				count=0
				name=r
				new_name=''
				tipo=''
				imo=''
				while count < len(title):
					if count == 0: # NOMBRE (TIPO)
						tmp_data=title[count].split('(')
						new_name = tmp_data[0].strip()
						tipo = tmp_data[1].replace(')','').strip()
					if count == 1: # IMO
						imo = title[count].replace('IMO','').strip()
					count+=1
				"""
				other_info=soup.find_all('li',{'class':'group-ib medium-gap line-120 vertical-offset-10'})
				#print(soup_i.find('title'))
				for info in other_info:
					#print(info)
					field=info.find('span',text=True, recursive=False)
					print(field)
					value=info.find('span').find('b').string
					print(value)
				"""
				#sleep(90)
				"""
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
				"""
				insert_data([imo,name,new_name,tipo])		
				buques.append({'imo':imo,'name':name,'new_name':new_name,'tipo':tipo})
			index+=1
	except Exception as e:
		insert_data(['No imo',r,r,'Container Ship'])
		buques.append({'imo':'No imo','name':name,'new_name':name,'tipo':'Container Ship'})
		index+=1
		print(e, "Data not found")
		continue
for buque in buques:
	print(buque)