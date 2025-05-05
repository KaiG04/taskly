from .common import *

DEBUG = True

SECRET_KEY = 'django-insecure-^j!%!pe-&9*%188@)3a1x2k0zyk*uhd8!nggutjgwl*mp&#)va'

DATABASES = {
    'default': {
        'ENGINE': 'django.db.backends.mysql',
        "OPTIONS": {
            "read_default_file": "taskly/settings/my.cnf",
        },
    }
}