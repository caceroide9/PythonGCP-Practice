import pymysql
from flask import jsonify
import requests

def open_connection():
    conn = pymysql.connect(user='', password='', unix_socket='/cloudsql/', db='', cursorclass=pymysql.cursors.DictCursor)
    return conn

def main(request):
  url = 'https://api.cameyo.com/'
  data = requests.get(url)
  if data.status_code==200:
    data2=data.json()
    for field_dict in data2['users']:
      _userId=field_dict['id']
      _userName=field_dict['userName']
      _role=field_dict['role']
      _status=field_dict['status']
      _groupName=field_dict['groupName']
      _groupId=field_dict['groupId']
      _expiration=field_dict['expiration']
      _metadata=field_dict['metadata']
      _powertags=field_dict['powertags']
      _created=field_dict['created']
      _lastActivity=field_dict['lastActivity']
      conn = open_connection()
      cur = conn.cursor(pymysql.cursors.DictCursor)
      cur.execute("INSERT INTO sesiones (userId,userName,role,status, groupName, groupId, expiration, metadata, powertags, created, lastActivity) VALUES (%s,%s,%s,%s,%s,%s,%s,%s,%s,%s,%s)", (_userId,_userName,_role,_status, _groupName, _groupId, _expiration, _metadata, _powertags, _created, _lastActivity))
      conn.commit()
