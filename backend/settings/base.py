from pathlib import Path
import os
from dotenv import load_dotenv

load_dotenv()  # add load_dotenv (without it I could not get the env vars working)

# Build paths inside the project like this: BASE_DIR / 'subdir'.
BASE_DIR = Path(__file__).resolve().parent.parent

# os.envion.get('EXAMPLE') method not working for me; 
DEBUG = os.environ.get('DEBUG')
SECRET_KEY = os.environ.get('SECRET_KEY')



# Other ways of getting env vars
# DEBUG = os.getenv("DEBUG")
# SECRET_KEY = os.getenv("SECRET_KEY")


STATIC_URL = '/static/'

STATIC_ROOT = os.path.join(BASE_DIR, 'static')

ALLOWED_HOSTS = ['*']