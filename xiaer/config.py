import os

class Configuration(object):
    APP_ROOT = os.path.dirname(os.path.realpath(__file__))
    SQLALCHEMY_DATABASE_URI = 'sqlite:///%s/xiaer.db' % APP_ROOT
    DEBUG = False
    SECRET_KEY = '&r4c*ig+hzp*e!_f)3&nh)zee^(=o)rp_+a-9ab5v*9n1*gr^n'
    MEDIA_ROOT = os.path.join(APP_ROOT, 'static')
    MEDIA_URL = '/static'