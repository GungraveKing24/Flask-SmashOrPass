from flask import Flask
from config import config
from flask_sqlalchemy import SQLAlchemy
from flask_migrate import migrate
import logging

app = Flask(__name__)
app.config.from_object(config)

db = SQLAlchemy(app)
migrate = migrate(app, db)

from app import routes, models

if not app.debug:
    stream_handler = logging.StreamHandler()
    stream_handler.setLevel(logging.INFO)
    app.logger.addHandler(stream_handler)

app.logger.setLevel(logging.INFO)
app.logger.info('Flask App Startup')