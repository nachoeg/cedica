from os import environ


class Config(object):
    TESTING = False
    SECRET_KEY = "algo"
    SESSION_TYPE = "filesystem"


class ProductionConfig(Config):
    MINIO_SERVER = environ.get("MINIO_SERVER")
    MINIO_ACCESS_KEY = environ.get("MINIO_ACCESS_KEY")
    MINIO_SECRET_KEY = environ.get("MINIO_SECRET_KEY")
    MINIO_SECURE = True
    SQLALCHEMY_DATABASE_URI = environ.get("DATABASE_URL")
    SQLALCHEMY_ENGINE_OPTIONS = {
        "pool_size": 10,
        "pool_recycle": 60,
        "pool_pre_ping": True,
    }


class DevelopmentConfig(Config):
    MINIO_SERVER = "127.0.0.1:9000"
    MINIO_ACCESS_KEY = "RCv2ATRvLe60Fa9rrzMy"
    MINIO_SECRET_KEY = "wFize5mJJ2G2VkmRZNwQQA3K7FanrqiQy9gZ7LFs"
    MINIO_SECURE = False
    DB_USER = "postgres"
    DB_PASSWORD = "postgres"
    DB_HOST = "localhost"
    DB_PORT = "5432"
    DB_NAME = "grupo17"
    SQLALCHEMY_DATABASE_URI = (
        f"postgresql://{DB_USER}:{DB_PASSWORD}@{DB_HOST}:{DB_PORT}/{DB_NAME}"
    )


class TestingConfig(Config):
    TESTING = True


config = {
    "development": DevelopmentConfig,
    "production": ProductionConfig,
    "testing": TestingConfig,
}
