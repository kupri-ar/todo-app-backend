from datetime import timedelta

ACCESS_EXPIRES = timedelta(hours=1)


class Config(object):
    DEBUG = True

    SQLALCHEMY_DATABASE_URI = 'postgresql://postgres:postgres@localhost:5432/postgres'
    SQLALCHEMY_TRACK_MODIFICATIONS = False

    JWT_SECRET_KEY = "super-secret-key"
    JWT_ACCESS_TOKEN_EXPIRES = ACCESS_EXPIRES
