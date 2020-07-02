from .base import *

ENV = 'Dev'
INSTALLED_APPS += [
    'users',
]

AUTH_USER_MODEL = 'users.UserInfo'
