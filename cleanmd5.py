import sqlite3
conn=sqlite3.connect('md5.db')
curs=conn.cursor()
curs.execute('''DROP TABLE md5_url''')
curs.close()
conn.close()