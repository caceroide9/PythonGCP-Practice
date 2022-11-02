import pymysql
from flask import jsonify
import requests
from datetime import date
from datetime import datetime
import datetime

def open_connection():
    conn = pymysql.connect(user='', password='', unix_socket='/cloudsql/', db='', cursorclass=pymysql.cursors.DictCursor)
    return conn

def main(request):
  url = 'https://api.cameyo.com/apps/'
  data = requests.get(url)
  if data.status_code==200:
    data2=data.json()
    for field_dict in data2['items']:
      _id=field_dict['id']
      _created=field_dict['created']
      _new_created=datetime.datetime.strptime(field_dict['created'], "%Y-%m-%dT%H:%M:%S.%f")
      _enabled=field_dict['enabled']
      _sessions=field_dict['sessions']
      _name=field_dict['name']
      _cluster=field_dict['cluster']
      _company=field_dict['company']
      _flags=field_dict['flags']
      _showInPortal=field_dict['showInPortal']
      conn = open_connection()
      cur = conn.cursor(pymysql.cursors.DictCursor)
      cur.execute("INSERT INTO apps_list (id_app,created,enabled,sessions,name,cluster,company,flags,showInPortal) VALUES (%s,%s,%s,%s,%s,%s,%s,%s,%s)", (_id,_new_created,_enabled,_sessions,_name,_cluster,_company,_flags,_showInPortal))
      conn.commit()
      
     
      
      
