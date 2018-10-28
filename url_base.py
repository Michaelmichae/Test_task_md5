import sqlite3
conn=sqlite3.connect('md5.db')
curs=conn.cursor()
curs.execute('''CREATE TABLE md5_url
(id VARCHAR(64) PRIMARY KEY,
url VARCHAR(2048),
status INT,
md5 VARCHAR(32),
email VARCHAR(255))''')
curs.close()
conn.close()