from backend.settings import DEBUG

DJANGO_APPS = [
    'django.contrib.admin',
    'django.contrib.auth',
    'django.contrib.contenttypes',
    'django.contrib.sessions',
    'django.contrib.messages',
    'django.contrib.staticfiles',
]

ON_TOP_APPS = [
    'corsheaders',
]

THIRD_PARTY_APPS = [
    'rest_framework',    
    'cacheops',
    'imagekit',
]

LOCAL_APPS = [
    'user',
    'collection',
    'document'
]

INSTALLED_APPS = ON_TOP_APPS + DJANGO_APPS + THIRD_PARTY_APPS + LOCAL_APPS

if DEBUG:
    INSTALLED_APPS += ['django_extensions']

DEFAULT_MIDDLEWARE = [
    'django.middleware.security.SecurityMiddleware',
    'django.contrib.sessions.middleware.SessionMiddleware',
    'django.middleware.common.CommonMiddleware',
    'django.middleware.csrf.CsrfViewMiddleware',
    'django.contrib.auth.middleware.AuthenticationMiddleware',
    'django.contrib.messages.middleware.MessageMiddleware',
    'django.middleware.clickjacking.XFrameOptionsMiddleware',
]

ON_TOP_MIDDLEWARE = ['corsheaders.middleware.CorsMiddleware', ]

# THIRD_PARTY_MIDDLEWARE = ['simple_history.middleware.HistoryRequestMiddleware']
THIRD_PARTY_MIDDLEWARE = []

LOCAL_MIDDLEWARE = [
    'base.middleware.RequestResponseLogMiddleware',
]

MIDDLEWARE = ON_TOP_MIDDLEWARE + DEFAULT_MIDDLEWARE + THIRD_PARTY_MIDDLEWARE + LOCAL_MIDDLEWARE

ROOT_URLCONF = 'backend.urls'

WSGI_APPLICATION = 'backend.wsgi.application'
