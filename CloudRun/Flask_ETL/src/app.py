from flask import Flask,jsonify,render_template,request
from config import config
from db import *



STATIC_FOLDER = 'templates/assets'
app = Flask(__name__,static_folder=STATIC_FOLDER)

@app.route('/', methods=['GET'])
def get_songs():
    return get()


@app.route('/add', methods=['POST'])
def add_song():
    if not request.is_json:
        return jsonify({"msg": "Missing JSON in request"}), 400

    create(request.get_json())
    return 'Song Added'

@app.route('/index')
def index():
    return render_template('layout.html')

@app.route('/complete')
def aux():
    return render_template('index.html', contacts=get2())


@app.route('/music', methods=['GET'])
def listar_cursos():
    return listmusic()
        
@app.route('/music/<codigo>', methods=['GET'])
def leer_curso(codigo):
    try:
        curso = leer_cancion(codigo)
        if curso != None:
            return curso
        else:
            return jsonify({'mensaje': "Curso no encontrado.", 'exito': False})
    except Exception as ex:
        return jsonify({'mensaje': "Error", 'exito': False})

@app.route('/music', methods=['POST'])
def registrar_curso():
    # print(request.json)
    try:
        curso = leer_cancion(request.json['codigo'])
        if curso != None:
            return jsonify({'mensaje': "Código ya existe, no se puede duplicar.", 'exito': False})
        else:
            post_cancion(request)
    except Exception as ex:
        return jsonify({'mensaje': "Error", 'exito': False})
        
@app.route('/cursos/<codigo>', methods=['PUT'])
def actualizar_curso(codigo):
    try:
        curso = leer_cancion(codigo)
        if curso != None:
            put_cancion(request,codigo)
        else:
            return jsonify({'mensaje': "Curso no encontrado.", 'exito': False})
    except Exception as ex:
        return jsonify({'mensaje': "Error", 'exito': False})

@app.route('/cursos/<codigo>', methods=['DELETE'])
def eliminar_curso(codigo):
    try:
        curso = leer_cancion(codigo)
        if curso != None:
            eliminar_cancion(codigo)
        else:
            return jsonify({'mensaje': "Curso no encontrado.", 'exito': False})
    except Exception as ex:
        return jsonify({'mensaje': "Error", 'exito': False})

if __name__ == "__main__":
    app.config.from_object(config['development'])
    app.run(host='0.0.0.0', port=8080,debug=True)