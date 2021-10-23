import os

from dotenv import load_dotenv


load_dotenv()


class Config:
    FLASK_APP = os.environ.get('FLASK_APP')
    FLASK_DEBUG = os.environ.get('DEBUG')
    SQLALCHEMY_DATABASE_URI = os.environ.get('DATABASE_URL')
