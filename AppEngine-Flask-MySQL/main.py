# main.py
from flask import Flask, jsonify, request,render_template
from db import get, create, get2

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




if __name__ == '__main__':
    app.run()
