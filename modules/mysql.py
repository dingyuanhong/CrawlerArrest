import MySQLdb

dbconfig = {'host':'192.168.205.128',
            'port': 3306,
            'user':'root',
            'passwd':'',
            'db':'mysql',
            'charset':'utf8'}

conn = MySQLdb.connect(host=dbconfig['host'],port=dbconfig['port'],user=dbconfig['user'],passwd=dbconfig['passwd'],db=dbconfig['db'],charset=dbconfig['charset']);
db=conn.cursor()
sql = "select * from user;"
param = None;
count = db.execute(sql,param)
records=db.fetchall()
print count;
print records;
db.close();
conn.close();
