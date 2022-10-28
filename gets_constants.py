import pyodbc,sys,os
import configparser

CONFIG_FILE = os.path.dirname(__file__) + '/buque.ini'
config = configparser.ConfigParser()
config.read(CONFIG_FILE)

DB_CONF = "Driver={ODBC Driver 11 for SQL Server};"+"Server="+config['CONFIG']['base_server']+"Database="+config['CONFIG']['base_db']+"UID="+config['CONFIG']['base_usr']+"PWD="+config['CONFIG']['base_pass']+ ";"

print("conexion realizada:Con exito\n")
def get_user_pass():
    list = []
    data = dict()
    try:
        cnxn = pyodbc.connect(DB_CONF)
        cursor = cnxn.cursor()
        sql = 'SELECT TOP 1 * FROM buques.dbo.TBL_Proxy_Users'

        cursor.execute(sql)
        columns = [column[0] for column in cursor.description]
        rows = cursor.fetchall()
        for row in rows:
            data = (dict(zip(columns, row)))
            list.append(data)
    except:
        data['domain_user'] = config['DEFAULT_USER']['base_usr']
        data['password'] = config['DEFAULT_USER']['base_pass']
        list.append(data)
    return list[0]

if __name__ == "__main__":

    print(get_user_pass())