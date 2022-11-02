import pymysql
from flask import jsonify
import requests
from datetime import date
from datetime import datetime
import pytz

def open_connection():
    conn = pymysql.connect(user='', password='', unix_socket='/cloudsql/', db='', cursorclass=pymysql.cursors.DictCursor)
    return conn

def main(request):
  user=""
  psw=""
  today = date.today().strftime("%Y-%m-%d")
  _today = date.today().strftime("%Y-%m-%d")
  serieDolar="F073.TCO.PRE.Z.D"
  url = "https://si3.bcentral.cl/+"
  response = requests.get(url)
  response2 = response.json()
  _descripEsp=response2["Series"]["descripEsp"]
  _descripIng=response2["Series"]["descripIng"]
  _seriesId=response2["Series"]["seriesId"]
  for data in response2["Series"]["Obs"]:
    _indexDateString=data["indexDateString"]
    _value=float(data["value"])
    _statusCode=data["statusCode"]
    country_time_zone = pytz.timezone('Chile/Continental')
    country_time = datetime.now(country_time_zone)
    x=country_time.strftime("%Y-%m-%d %H:%M:%S")
    y=datetime.strptime(x, "%Y-%m-%d %H:%M:%S")
    op=datetime.strptime(_indexDateString, "%d-%m-%Y")
    r=op.date()
    conn = open_connection()
    cur = conn.cursor(pymysql.cursors.DictCursor)
    cur.execute("INSERT INTO monedasObservadas (descripEsp,descripIng,seriesId,indexDateString,value,statusCode,today) VALUES (%s,%s,%s,%s,%s,%s,%s)", (_descripEsp,_descripIng,_seriesId, r,_value,_statusCode,y))
    conn.commit()


    



  
  


 
  
  

         

      

