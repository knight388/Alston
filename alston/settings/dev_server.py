
"""
settings module for dev

set env var
DJANGO_SETTINGS_MODULE=alston.settings.dev_server
"""
import django

from alston.settings.base import *

import django

from alston.settings.base import *

DB_USER = 'root'
DB_PWD = 'mysql'
DB_HOST = 'localhost'

django.setup()

for db in DATABASES:
	DATABASES[db]['USER'] = DB_USER
	DATABASES[db]['PASSWORD'] = DB_PWD
	DATABASES[db]['HOST'] = DB_HOST
