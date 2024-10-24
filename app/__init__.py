from flask import Flask
from config import Config
from flask_sqlalchemy import SQLAlchemy
from flask_migrate import Migrate
from datetime import timedelta
from authlib.integrations.flask_client import OAuth
import logging

app = Flask(__name__)
app.config.from_object(Config)
oauth = OAuth(app)
app.secret_key = ',aos844a/scña{scasñsaç.ñasasdci-{,añc,.c{ñasc'  # Cambia esto por una clave segura
app.permanent_session_lifetime = timedelta(minutes=30)  # Establece la duración de la sesión
app.config['SESSION_COOKIE_SAMESITE'] = 'None'  # Cambia a 'Lax' si solo necesitas seguridad en la misma pestaña
app.config['SESSION_COOKIE_SECURE'] = True
db = SQLAlchemy(app)
migrate = Migrate(app, db)

oauth.register(
    name='google',
    client_id=app.config['GOOGLE_CLIENT_ID'],
    client_secret=app.config['GOOGLE_CLIENT_SECRET'],
    access_token_url='https://accounts.google.com/o/oauth2/token',
    authorize_url='https://accounts.google.com/o/oauth2/auth',
    authorize_params=None,
    access_token_params=None,
    jwks_uri='https://www.googleapis.com/oauth2/v3/certs',
    redirect_uri='http://127.0.0.1:5000/auth/callback/google',   
    client_kwargs={'scope': 'openid profile email'}
)

from app import routes, models

if not app.debug:
    stream_handler = logging.StreamHandler()
    stream_handler.setLevel(logging.INFO)
    app.logger.addHandler(stream_handler)

app.logger.setLevel(logging.INFO)
app.logger.info('Flask App Startup')