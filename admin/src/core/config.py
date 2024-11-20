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
    TABLA_CANT_FILAS = environ.get("TABLA_CANT_FILAS")
    GOOGLE_CLIENT_ID = ""
    GOOGLE_CLIENT_SECRET = ""


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
    TABLA_CANT_FILAS = 6
    GOOGLE_CLIENT_ID = "990473437871-efj1b23nan95nnvar20oi2dj3fgr18gj.apps.googleusercontent.com"
    GOOGLE_CLIENT_SECRET = "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"


class TestingConfig(Config):
    TESTING = True


config = {
    "development": DevelopmentConfig,
    "production": ProductionConfig,
    "testing": TestingConfig,
}
