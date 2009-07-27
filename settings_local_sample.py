import os


PROJECT_PATH = os.path.normpath(os.path.join(os.path.dirname(os.path.realpath(__file__))))

DEBUG = True
TEMPLATE_DEBUG = DEBUG
LOCAL_DEVELOPMENT = True

DATABASE_ENGINE = 'sqlite3'
DATABASE_NAME = os.path.join(PROJECT_PATH, '..', '..', 'db', 'foia.sqlite')
DATABASE_USER = ''
DATABASE_PASSWORD = ''
DATABASE_HOST = ''
DATABASE_PORT = ''