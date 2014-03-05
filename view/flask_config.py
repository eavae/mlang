#encoding:utf-8
import sae.const

class Config(object):
    SQLALCHEMY_DATABASE_URI = 'mysql://%s:%s@%s:%s/%s' % (
        sae.const.MYSQL_USER,
        sae.const.MYSQL_PASS,
        sae.const.MYSQL_HOST,
        sae.const.MYSQL_PORT,
        sae.const.MYSQL_DB,
        )
    BABEL_DEFAULT_LOCALE = 'en'
    BABEL_DEFAULT_TIMEZONE = 'Asia/Shanghai'
    QQMAIL_ACCOUNT = '823979282'
    QQMAIL_PASSWORD = 'lijingyulfx*'
    MAILUUID_EXIST_TIME = 7*24*60*60
    DEFAULT_USER_AUTH = True
    TEXT_MAX_LENGTH = 10000
    SERVER_NAME = 'localhost'
    SQLALCHEMY_POOL_RECYCLE = 3600
    MAX_CONTENT_LENGTH = 16 * 1024 * 1024
    STORAGE_NAME = 'mlang'
    AVATAR_SIZE_S = 48
    AVATAR_SIZE_M = 96
    AVATAR_SIZE_L = 192
    DEFAULT_AVATAR_URL = '/img/avatar/'

class DevConfig(Config):
    DEBUG = True
    HOST_URL = 'http://localhost:8080'
    SERVER_NAME = 'localhost:8080'

class ProdConfig(Config):
    DEBUG = False
    BABEL_DEFAULT_LOCALE = 'en'
    HOST_URL = "http://mlang.sinaapp.com/"
    SERVER_NAME = 'mlang.sinaapp.com'
