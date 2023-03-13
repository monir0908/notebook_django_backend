import os

# django vars
AUTH_USER_MODEL = 'user.User'
LANGUAGE_CODE = 'en-us'
LANG="en_US.utf8"
LC_ALL="en_US.UTF-8"
LC_LANG="en_US.UTF-8"
TIME_ZONE = 'UTC'
USE_I18N = True
USE_L10N = True
USE_TZ = True
APPEND_SLASH = False
STATIC_URL = '/static/'
MAX_FILE_SIZE = 100 * 1024 * 1024  # 5MB
# env
DB_NAME = os.environ.get('DB_NAME')
DB_USER = os.environ.get('DB_USER')
DB_PASS = os.environ.get('DB_PASSWORD')
DB_HOST = os.environ.get('DB_HOST')
# DB_PORT = int(os.environ.get('DB_PORT'))
DB_PORT = os.environ.get('DB_PORT')

# request setup
REQUEST_TIMEOUT = int(os.environ.get('REQUEST_TIMEOUT', 8))
