import os

class Config:
    SECRET_KEY = os.environ.get('SECRET_KEY', os.urandom(24))
    SQLALCHEMY_DATABASE_URI = os.getenv('Database_URL', 'postgresql://default:JLHW0egO3Iaq@ep-super-brook-a4u8no3k-pooler.us-east-1.aws.neon.tech:5432/verceldb?sslmode=require')
    SQLALCHEMY_TRACK_MODIFICATIONS = False
    GOOGLE_OAUTH_CLIENT_ID = os.getenv('GOOGLE_OAUTH_CLIENT_ID')
    GOOGLE_OAUTH_CLIENT_SECRET = os.getenv('GOOGLE_OAUTH_CLIENT_SECRET')
