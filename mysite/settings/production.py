from .base import *
import os

DEBUG = os.environ.get('DEBUG', 'False') == 'True'
SECRET_KEY = os.environ.get('SECRET_KEY')
ALLOWED_HOSTS = [
    'localhost',
    '127.0.0.1',
    'eja-blog.up.railway.app',
    'myblog-nes7.onrender.com',
    '.onrender.com',
]

CSRF_TRUSTED_ORIGINS = [
    'https://eja-blog.up.railway.app',
    'https://myblog-nes7.onrender.com',
    'https://.onrender.com',
]

STORAGES = {
    "default": {
        "BACKEND": "django.core.files.storage.FileSystemStorage",
    },
    "staticfiles": {
        "BACKEND": "whitenoise.storage.CompressedManifestStaticFilesStorage",
    },
}
