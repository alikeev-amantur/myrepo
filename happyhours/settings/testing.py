import sys

from .base import *

DEBUG = True

DATABASES = {
  'default': {
      'ENGINE': 'django.contrib.gis.db.backends.postgis',
      'NAME': 'myapp',
      'USER': 'myuser',
      'PASSWORD': 'mypassword',
      'HOST': 'db',
      'PORT': '5432',
  }
}


if 'test' in sys.argv or 'test_coverage' in sys.argv:
    DATABASES['default']['NAME'] = 'test_myapp'
