import hashlib
import sqlite3
import requests
import uuid
import json
import urllib
import os
import threading
import time
import smtplib
from flask import Flask
from flask import request
app=Flask(__name__)
statuses=dict()
statuses[0]='no such task'
statuses[1]='running'
statuses[2]='done'
statuses[3]='error'
server=smtplib.SMTP('smtp.gmail.com',587)
server.connect('smtp.gmail.com',25)
server.starttls()
email_account_login = "insert_emaillogin_there"
email_account_password = "insert_emailpassword_there"
server.login(email_account_login, email_account_password)
def check_download():
    conn = sqlite3.connect('md5.db')
    curs = conn.cursor()
    while True:
        curs.execute('SELECT id,url,status,md5,email from md5_url WHERE status=?', [1])
        inf=curs.fetchall()
        if len(inf)==0:
            time.sleep(5)
            continue
        id=inf[0][0]
        url=inf[0][1]
        sum = download(inf[0][1], 'downloads/' + id)
        curs.execute('UPDATE md5_url SET status=2,md5=? WHERE id=? ', [sum, id])
        conn.commit()
        email=inf[0][4]
        if email!='':
            try:
                mail='\n'+'url='+url+'\n'+'md5_sum='+sum
                server.sendmail(email_account_login, email, mail)
            except Exception as e:
                print('Error!'+str(e))
        time.sleep(5)
    conn.close()
    return

#статус: 1-задача в работе,2- законченная задача,3-ошибка выполнения
md5_thread=threading.Thread(target=check_download,args=())
md5_thread.daemon = True
md5_thread.start()

def download_and_calculate(url, file_path):
    urllib.request.urlretrieve(url, file_path)
    sum = hashlib.md5(open(file_path, 'rb').read()).hexdigest()
    os.remove(file_path)
    return sum


def download(url, file_name):
    # open in binary mode
    with open(file_name, "wb") as file:
        # get request
        response = requests.get(url)
        # write to file
        file.write(response.content)
    sum = hashlib.md5(open(file_name, 'rb').read()).hexdigest()
    os.remove(file_name)
    return sum

@app.route('/submit', methods=['POST'])
def submit_url():
    conn = sqlite3.connect('md5.db')
    curs = conn.cursor()
    url=request.form['url']
    email=request.form['email']
    ins = 'INSERT INTO md5_url (id,url,status,md5,email) VALUES(?,?,?,?,?)'
    id=str(uuid.uuid4())
    curs.execute(ins,[id,url,1,'',email])
    conn.commit()
    response=dict()
    response['id']=id
    curs.close()
    conn.close()
    return json.dumps(response)

@app.route('/check', methods=['GET'])
def check():
    global ststuses
    conn = sqlite3.connect('md5.db')
    curs = conn.cursor()
    id_check=request.args.get('id','')
    curs.execute('SELECT id,url,status,md5,email from md5_url WHERE id=?',[id_check])
    inf=curs.fetchall()
    status=0
    if len(inf)>0:
        status=inf[0][2]
    response=dict()
    if status==2:
        response['url']=inf[0][1]
        response['md5']=inf[0][3]
    response['status']=statuses[status]
    curs.close()
    conn.close()
    return json.dumps(response)




