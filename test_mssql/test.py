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
sql = "select IDNO,CHECKTIME_IN,CHECKTIME_OUT from ANVIZ_ABS_FOR_ODOO"
cur.execute(sql)
records = cur.fetchall()

"""
[id]
      ,[LOC_IN]
      ,[LOC_OUT]
      ,[IDNO]
      ,[NAME]
      ,[CHECKTIME_IN]
      ,[CHECKTIME_OUT]
      ,[IN]
      ,[OUT]
      ,[RMK]
      ,[FINAL_RMK]
      ,[DESC]
      ,[SDESC]
      ,[SHIFT]
      ,[DT_TIME]
      ,[TIMEINWCA]
      ,[TIMEOUTWCA]
      ,[GRPDSC]
"""

#---- process results
sql = """insert into hr_attendance (employee_id, check_in, check_out) VALUES """
values= []
for rec in records:
    IDNO = rec[0]
    CHECKTIME_IN=rec[1]
    CHECKTIME_OUT=rec[2]
    values.append (str((IDNO, CHECKTIME_IN, CHECKTIME_OUT)) )

sql = sql + ",".join(values)

print(sql)
