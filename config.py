import os

class Config:
    SECRET_KEY = os.environ.get('SECRET_KEY', os.urandom(32))
    SQLACHEMY_DATABASE_URI = os.getenv('DATABASE_URL', 'POSTGRES_DB_URL')
    SQLACHEMY_TRACK_MODIFICATIONS = False