"""
settings module for nbb

set env var
DJANGO_SETTINGS_MODULE=alston.settings.nbb
"""
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
