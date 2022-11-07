import os
import pymysql
from flask import jsonify

#db_user = os.environ.get('CLOUD_SQL_USERNAME')
#db_password = os.environ.get('CLOUD_SQL_PASSWORD')
#db_name = os.environ.get('CLOUD_SQL_DATABASE_NAME')
#db_connection_name = os.environ.get('CLOUD_SQL_CONNECTION_NAME')


def open_connection():
    conn = pymysql.connect(user='mcaceres',password='Mathias.2022',unix_socket='/cloudsql/mysql-prueba-318822:us-central1:test-appsheet',db='music',cursorclass=pymysql.cursors.DictCursor)
    #conn=  pymysql.connect(host='35.193.37.196',user='mcaceres',password='Mathias.2022',database='music',port=3306)
    return conn


def get():
    conn = open_connection()
    with conn.cursor() as cursor:
        result = cursor.execute('SELECT * FROM songs;')
        songs = cursor.fetchall()
        if result > 0:
            got_songs = jsonify(songs)
        else:
            got_songs = 'No Songs in DB'
        return got_songs


def create(song):
    conn = open_connection()
    with conn.cursor() as cursor:
        cursor.execute('INSERT INTO songs (title, artist, genre) VALUES(%s, %s, %s)',
                       (song["title"], song["artist"], song["genre"]))
    conn.commit()
    conn.close()


def get2():
    conn = open_connection()
    with conn.cursor() as cursor:
        result = cursor.execute('SELECT * FROM songs;')
        songs = cursor.fetchall()
        if result > 0:
            got_songs = (songs)
        else:
            got_songs = 'No Songs in DB'
        return got_songs


def listmusic():
    try:
        conn = open_connection()
        with conn.cursor() as cursor:
            sql = "SELECT title, artist, genre FROM songs ORDER BY nombre ASC"
            cursor.execute(sql)
            datos = cursor.fetchall()
            cursos = []
            for fila in datos:
                curso = {'title': fila[0], 'artist': fila[1], 'genre': fila[2]}
                cursos.append(curso)
        return cursos
    except Exception as ex:
        return ({'mensaje': "Error", 'exito': False})


def leer_cancion(codigo):
    try:
        conn = open_connection()
        with conn.cursor() as cursor:
            sql = "SELECT title, artist, genre FROM songs WHERE title = '{0}'".format(codigo)
            cursor.execute(sql)
            datos = cursor.fetchone()
            if datos != None:
                curso = {'title': datos[0], 'artist': datos[1], 'genre': datos[2]}
                return curso
            else:
                return None
        
    except Exception as ex:
        raise ex


def post_cancion(request):
    conn = open_connection()
    with conn.cursor() as cursor:
        sql = """INSERT INTO songs (title, artist, genre) 
             VALUES ('{0}', '{1}', {2})""".format(request.json['title'],
                                                     request.json['artist'], request.json['genre'])
    cursor.execute(sql)
    conn.connection.commit()  # Confirma la acción de inserción.
    return jsonify({'mensaje': "Curso registrado.", 'exito': True})

def put_cancion(request,codigo):
    conn = open_connection()
    with conn.cursor() as cursor:
        sql = """UPDATE curso SET artist = '{0}', genre = {1} 
                WHERE title = '{2}'""".format(request.json['artist'], request.json['genre'], codigo)
        cursor.execute(sql)
        conn.connection.commit()  # Confirma la acción de actualización.
        return jsonify({'mensaje': "Curso actualizado.", 'exito': True})

def eliminar_cancion(codigo):
    conn = open_connection()
    with conn.cursor() as cursor:
        sql = "DELETE FROM curso WHERE codigo = '{0}'".format(codigo)
        cursor.execute(sql)
        conn.connection.commit()  # Confirma la acción de eliminación.
        return jsonify({'mensaje': "Curso eliminado.", 'exito': True})