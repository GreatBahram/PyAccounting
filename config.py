import os


class Config:
    DEBUG = False
    TESTING = False
    CURRENT_PATH = os.path.dirname(__file__)
    DATABASE_URI = ""
    WTF_CSRF_ENABLED = True
    SECRET_KEY = "Bahram"


class DevelopmentConfig(Config):
    DEBUG = True
    DATABASE_URI = ":memory:"


class TestingConfig(Config):
    TESTING = True
    DATABASE_URI = ":memory:"


class ProductionConfig(Config):
    DATABASE_URI = Config.CURRENT_PATH + "database.db"

