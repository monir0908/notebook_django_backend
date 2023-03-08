from backend.settings import DB_NAME, DB_USER, DB_PASS, DB_HOST, DB_PORT

DATABASES = {
    'default': {
        'ENGINE': 'django.db.backends.postgresql_psycopg2',
        'NAME': DB_NAME,
        'USER': DB_USER,
        'PASSWORD': DB_PASS,
        'HOST': DB_HOST,
        'PORT': DB_PORT,
    }
}

# # To use sqlite3 database
# # --------------------------
# # Build paths inside the project like this: BASE_DIR / 'subdir'.
# from pathlib import Path
# BASE_DIR = Path(__file__).resolve().parent.parent


# DATABASES = {
#     'default': {
#         'ENGINE': 'django.db.backends.sqlite3',
#         'NAME': BASE_DIR / 'db.sqlite3',
#     }
# }