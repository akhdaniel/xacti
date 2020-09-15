import pypyodbc

ip_address="172.17.145.17"
user="user_postgresql"
password="Postgresql"
port="1433"
database="HRD"

#---- connection and create cursor
cs='DRIVER={ODBC Driver 17 for SQL Server};PORT='+port+';SERVER='+ip_address+';DATABASE='+database+';UID='+user+';PWD='+password
cnn = pypyodbc.connect(cs, unicode_results=True)
cur = cnn.cursor()

#---- query database
sql = "select * from ANVIZ_ABS_FOR_ODOO"
cur.execute(sql)
records = cur.fetchall()

#---- process results
print(records)
