import base64


class BaseConfig(object):
    SQLALCHEMY_TRACK_MODIFICATIONS = True
    DEBUG = True
    SECRET_KEY = '\x167\xd3\x03e"\x1b\x9c\x01\xfb\xc0\x9b\x84\xa9\x0e\x7fS\x07\xa5S\xf3\xd6\x89'
    # DB Configs:
    DATABASE_URI = 'postgres+psycopg2://postgres:Ts4f34pp!@3@157.230.183.79:5432/postgres'
    MAX_CONTENT_LENGTH = 16 * 1024 * 1024

