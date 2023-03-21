from pathlib import Path
import os
from dotenv import load_dotenv

load_dotenv()  # add load_dotenv (without it I could not get the env vars working)

# Build paths inside the project like this: BASE_DIR / 'subdir'.
# BASE_DIR = Path(__file__).resolve().parent.parent
# BASE_DIR = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))
BASE_DIR = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))

# go up one more level to reach the root directory of your project
BASE_DIR = os.path.dirname(BASE_DIR)


# os.envion.get('EXAMPLE') method not working for me; 
DEBUG = os.environ.get('DEBUG', False) == 'True'
SECRET_KEY = os.environ.get('SECRET_KEY')

# Other ways of getting env vars
# DEBUG = os.getenv("DEBUG")
# SECRET_KEY = os.getenv("SECRET_KEY")

ALLOWED_HOSTS = ['*']

STATIC_URL = '/static/'
STATIC_ROOT = os.path.join(BASE_DIR, 'staticfiles')
STATICFILES_DIRS = [
    os.path.join(BASE_DIR, 'static'),
]

MEDIA_ROOT = os.path.join(BASE_DIR, 'media')
MEDIA_URL = '/media/'


DEFAULT_FILE_STORAGE = 'django.core.files.storage.FileSystemStorage'

# Maximum file size in bytes
MAX_FILE_SIZE = 5 * 1024 * 1024

# List of valid file extensions
VALID_EXTENSIONS = ['.pdf', '.doc', '.docx', '.xls', '.xlsx', '.ppt', '.pptx', '.jpg', '.jpeg', '.png', '.gif']

# EMAIL SETTINGS
FRONTEND_URL = os.environ.get('FRONTEND_URL')
EMAIL_BACKEND = os.environ.get('EMAIL_BACKEND')
EMAIL_HOST = os.environ.get('EMAIL_HOST')
EMAIL_PORT = os.environ.get('EMAIL_PORT')
EMAIL_HOST_USER = os.environ.get('EMAIL_HOST_USER')
EMAIL_HOST_PASSWORD = os.environ.get('EMAIL_HOST_PASSWORD')
EMAIL_USE_TLS = os.environ.get('EMAIL_USE_TLS', False) == 'True'


TEMPLATES_DIR = os.path.join(BASE_DIR, 'templates') # as settings is a folder (not a file) and all its files reside under settings folder
TEMPLATES = [
    {
        'BACKEND': 'django.template.backends.django.DjangoTemplates',
        'DIRS': [TEMPLATES_DIR],
        'APP_DIRS': True,
        'OPTIONS': {
            'context_processors': [
                'django.template.context_processors.debug',
                'django.template.context_processors.request',
                'django.contrib.auth.context_processors.auth',
                'django.contrib.messages.context_processors.messages',
            ],
        },
    },
]