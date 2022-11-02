from flask import Flask,jsonify,render_template,request
from config import config
from db import *
from flask import Flask
import folium
import pandas as pd 
from folium.plugins import MarkerCluster

app = Flask(__name__)


conn = pymysql.connect(user='',password='',unix_socket='/cloudsql/',db='',cursorclass=pymysql.cursors.DictCursor)
#conn=  pymysql.connect(host='',user='',password='',database='',port=)


@app.route("/")
def base():
    # this is base map
    df = pd.read_sql_query("SELECT * FROM Punto",conn)
    df.columns= df.columns.str.strip()
    subset_of_df=df.sample(n=5)
    some_map= folium.Map(location=[subset_of_df['Y'].mean(),subset_of_df['X'].mean()],zoom_start=10)
    for row in subset_of_df.itertuples():
        some_map.add_child(folium.Marker(location=[row.Y,row.X],popup=row.ID))
    some_map_2= folium.Map(location=[subset_of_df['Y'].mean(),subset_of_df['X'].mean()],zoom_start=10)
    mc=MarkerCluster()
    for row in subset_of_df.itertuples():
        mc.add_child(folium.Marker(location=[row.Y,row.X],popup=row.ID))
    some_map_2.add_child(mc)
    return some_map_2._repr_html_()


if __name__ == "__main__":
    app.config.from_object(config['development'])
    app.run(host='0.0.0.0', port=8080,debug=True)





