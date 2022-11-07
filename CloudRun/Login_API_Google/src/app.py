import os
import pathlib
import requests
from flask import Flask, session, abort, redirect, request
from google.oauth2 import id_token
from google_auth_oauthlib.flow import Flow
from pip._vendor import cachecontrol
import google.auth.transport.requests
import logging
import os
from typing import Union
from google.cloud import storage
import pymysql
from datetime import date
from datetime import datetime
import pytz

app = Flask("Google Login App")
app.secret_key = "Sofruco.Team"

os.environ["OAUTHLIB_INSECURE_TRANSPORT"] = "1"
#Colocar cliente de la api
GOOGLE_CLIENT_ID = "123"
#Directorio del json
client_secrets_file = os.path.join(pathlib.Path(__file__).parent, "123.json")


CLOUD_STORAGE_BUCKET = 'agroweb'

flow = Flow.from_client_secrets_file(
    client_secrets_file=client_secrets_file,
    scopes=["https://www.googleapis.com/auth/userinfo.profile", "https://www.googleapis.com/auth/userinfo.email", "openid"],
    redirect_uri="url/callback"
    ###Es importante destacar que en este linea hay que ir colocando lo necesario para que responda el servicio ya sea por la url que da por defecto el cloud run o el dns
)


def login_is_required(function):
    def wrapper(*args, **kwargs):
        if "google_id" not in session:
            return abort(401)  # Authorization required
        else:
            return function()

    return wrapper

def open_connection():
    conn = pymysql.connect(user='1',password='2',unix_socket='3',db='4',cursorclass=pymysql.cursors.DictCursor)
    return conn

def create(_campo):
    conn = open_connection()
    with conn.cursor() as cursor:
        cursor.execute('INSERT INTO tabla (campos) VALUES(%s)',
                       (_campo ))
    conn.commit()
    conn.close()

@app.route("/login")
def login():
    authorization_url, state = flow.authorization_url()
    session["state"] = state
    return redirect(authorization_url)


@app.route("/callback")
def callback():
    flow.fetch_token(authorization_response=request.url)

    if not session["state"] == request.args["state"]:
        abort(500)  # State does not match!

    credentials = flow.credentials
    request_session = requests.session()
    cached_session = cachecontrol.CacheControl(request_session)
    token_request = google.auth.transport.requests.Request(session=cached_session)

    id_info = id_token.verify_oauth2_token(
        id_token=credentials._id_token,
        request=token_request,
        audience=GOOGLE_CLIENT_ID
    )

    session["google_id"] = id_info.get("sub")
    session["name"] = id_info.get("name")
    return redirect("/protected_area")


@app.route("/logout")
def logout():
    session.clear()
    return redirect("/")


@app.route("/")
def index():
    
    return "Hello World <a href='/login'><button>Login</button></a>"


@app.route("/protected_area")
@login_is_required
def protected_area():
    return f"Hola {session['name']}! <br/> <a href='/logout'><button>Logout</button></a>" """<form method="POST" action="/upload" enctype="multipart/form-data">
    <input type="file" name="file">
    <input type="submit">
</form>
"""

@app.route('/upload', methods=['POST'])
def upload() -> str:
    
    """Process the uploaded file and upload it to Google Cloud Storage."""
    uploaded_file = request.files.get('file')

    if not uploaded_file:
        return 'No file uploaded.', 400

    # Create a Cloud Storage client.
    gcs = storage.Client()

    # Get the bucket that the file will be uploaded to.
    bucket = gcs.get_bucket(CLOUD_STORAGE_BUCKET)

    # Create a new blob and upload the file's content.
    blob = bucket.blob(uploaded_file.filename)

    blob.upload_from_string(
        uploaded_file.read(),
        content_type=uploaded_file.content_type
    )

    # Make the blob public. This is not necessary if the
    # entire bucket is public.
    # See https://cloud.google.com/storage/docs/access-control/making-data-public.
    blob.make_public()

    # The public URL can be used to directly access the uploaded file via HTTP.
    country_time_zone = pytz.timezone('Chile/Continental')
    country_time = datetime.now(country_time_zone)
    x=country_time.strftime("%Y-%m-%d %H:%M:%S")
    y=datetime.strptime(x, "%Y-%m-%d %H:%M:%S")
    create(session['name'])
    return blob.public_url


@app.errorhandler(500)
def server_error(e: Union[Exception, int]) -> str:
    logging.exception('An error occurred during a request.')
    return """
    An internal error occurred: <pre>{}</pre>
    See logs for full stacktrace.
    """.format(e), 500


if __name__ == "__main__":
    app.run(host='0.0.0.0', port=80,debug=True)