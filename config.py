import os

from dotenv import load_dotenv


load_dotenv()


class Config:
    FLASK_APP = os.environ.get('FLASK_APP')
    SECRET_KEY = os.environ.get('SECRET_KEY')
    FLASK_DEBUG = os.environ.get('DEBUG')
    SQLALCHEMY_DATABASE_URI = os.environ.get('DATABASE_URL')
    SQLALCHEMY_TRACK_MODIFICATIONS = os.environ.get('SQLALCHEMY_TRACK_MODIFICATIONS')
    MAIL_SERVER = os.environ.get('MAIL_SERVER')
    MAIL_PORT = os.environ.get('MAIL_PORT')
    MAIL_USE_TLS = os.environ.get('MAIL_USE_TLS')
    MAIL_USERNAME = os.environ.get('MAIL_USERNAME')
    MAIL_PASSWORD = os.environ.get('MAIL_PASSWORD')
    ADMINS = os.environ.get('ADMINS')
    FLASK_ADMIN_SWATCH = 'cerulean'
    ADS_PER_PAGE = int(os.environ.get('ADS_PER_PAGE'))
