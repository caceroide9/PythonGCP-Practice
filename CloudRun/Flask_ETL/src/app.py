from flask import Flask,jsonify,render_template

from config import config
from flask_mysqldb import MySQL


STATIC_FOLDER = 'templates/assets'
app = Flask(__name__,static_folder=STATIC_FOLDER)
conexion= MySQL(app)

@app.route('/',methods=['GET'])
def ping():
    return render_template("index.html")

if __name__ == "__main__":
    app.config.from_object(config['development'])
    app.run(host='0.0.0.0', port=8080,debug=True) 