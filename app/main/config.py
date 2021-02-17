import os
import urllib.parse 
import pyodbc

secret = "q68epcrUK0Qfap33dve0pOlI6nPgjxHT"

# Procura driver atual do SQL Server
drivers = [item for item in pyodbc.drivers()]
driver = drivers[-1]

# Dados acesso banco de dados
server = '35.199.101.9'
database = 'dbIconnectCameraFrame'
uid = 'iconnect'
pwd = 'FGHr$!56'

connection_link_str = f'DRIVER={driver};SERVER={server};DATABASE={database};UID={uid};PWD={pwd}'
params = urllib.parse.quote_plus(connection_link_str)


class Config:
    SECRET_KEY = os.getenv('SECRET_KEY', secret)
    DEBUG = False


class DevelopmentConfig(Config):
    DEBUG = True
    TESTING = True
    SQLALCHEMY_DATABASE_URI = "mssql+pyodbc:///?odbc_connect=%s" % params
    SQLALCHEMY_TRACK_MODIFICATIONS = False
    SESSION_COOKIE_DOMAIN = False
    SERVER_NAME = "172.16.2.140:1882"
    CORS_HEADERS = "Content-Type"


class TestingConfig(Config):
    DEBUG = True
    TESTING = True
    SQLALCHEMY_DATABASE_URI = "mssql+pyodbc:///?odbc_connect=%s" % params
    PRESERVE_CONTEXT_ON_EXCEPTION = False
    SQLALCHEMY_TRACK_MODIFICATIONS = False


class ProductionConfig(Config):
    DEBUG = False
    # uncomment the line below to use postgres
    # SQLALCHEMY_DATABASE_URI = postgres_local_base


config_by_name = dict(
    dev=DevelopmentConfig,
    test=TestingConfig,
    prod=ProductionConfig
)

key = Config.SECRET_KEY
