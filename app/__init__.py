from flask import Flask
from config import Config
from flask_sqlalchemy import SQLAlchemy
from flask_migrate import Migrate
from datetime import timedelta
import logging

app = Flask(__name__)
app.config.from_object(Config)
app.secret_key = ',aos844a/scña{scasñsaç.ñasasdci-{,añc,.c{ñasc'  # Cambia esto por una clave segura
app.permanent_session_lifetime = timedelta(minutes=30)  # Establece la duración de la sesión
app.config['SESSION_COOKIE_SAMESITE'] = 'None'  # Cambia a 'Lax' si solo necesitas seguridad en la misma pestaña
app.config['SESSION_COOKIE_SECURE'] = True
db = SQLAlchemy(app)
migrate = Migrate(app, db)

from app import routes, models

if not app.debug:
    stream_handler = logging.StreamHandler()
    stream_handler.setLevel(logging.INFO)
    app.logger.addHandler(stream_handler)

app.logger.setLevel(logging.INFO)
app.logger.info('Flask App Startup')