class Config:
    """
    Common configurations
    Put any configurations here that are common across all environments
    """
    DEBUG = False
    TESTING = False
    SQLALCHEMY_TRACK_MODIFICATIONS = False


class DevelopmentConfig(Config):
    """
    Development configurations
    """
    DEBUG = True
    SQLALCHEMY_ECHO = True
    SECRET_KEY = "FakeK3y"
    SQLALCHEMY_DATABASE_URI = "sqlite:///../database.db"


class TestingConfig(Config):
    """
    Testing configurations
    """
    TESTING = True


class ProductionConfig(Config):
    """
    Production configurations
    """

app_config = {
        'development': DevelopmentConfig,
        'production': ProductionConfig,
        'testing': TestingConfig,
        }
