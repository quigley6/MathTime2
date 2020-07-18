import os
basedir = os.path.abspath(os.path.dirname(__file__))

class Config(object):
    SECRET_KEY = 'asldkfja0s9ed8f0823jpiefasd98u'

    SQLALCHEMY_DATABASE_URI = 'sqlite:///' + os.path.join(basedir, 'MathTime2.db')
    SQLALCHEMY_TRACK_MODIFICATIONS  = False
