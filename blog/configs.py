import os


basedir = os.path.abspath(os.path.dirname(__file__))


class BaseConfig(object):
    DEBUG = False
    TESTING = False
    SQLALCHEMY_DATABASE_URI = 'sqlite:///' + \
        os.path.join(basedir, 'blog.db')
    SQLALCHEMY_TRACK_MODIFICATIONS = False
    SECRET_KEY = "abcdefg123456"
    WTF_CSRF_ENABLED = True


class DevConfig(BaseConfig):
    DEBUG = True
    SQLALCHEMY_DATABASE_URI = os.environ.get("SQLALCHEMY_DATABASE_URI")


class TestingConfig(BaseConfig):
    TESTING = True
