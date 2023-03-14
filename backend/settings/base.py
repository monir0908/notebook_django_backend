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
DEBUG = os.environ.get('DEBUG')
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



# Maximum file size in bytes
MAX_FILE_SIZE = 5 * 1024 * 1024

# List of valid file extensions
VALID_EXTENSIONS = ['.pdf', '.doc', '.docx', '.xls', '.xlsx', '.ppt', '.pptx', '.jpg', '.jpeg', '.png', '.gif']
DEFAULT_FILE_STORAGE = 'django.core.files.storage.FileSystemStorage'
