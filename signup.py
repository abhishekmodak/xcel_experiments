import hashlib
import random
import string
import time
import datetime
import logging
from django.contrib.auth import authenticate
from django.contrib.auth import login as django_login
from django.contrib.auth.models import User, UserManager
from django.db import IntegrityError
from django.utils import timezone

from tastypie.models import ApiKey

from accounts import exceptions
#from entity_curation.mod import init_logger
from scripts.init_logger import init_log


# Public
######################

#LOG_FILE = '/home/veveo/CURATION_TOOL/LOGS/accounts%s.log' % str(datetime.datetime.now())
LOG_FILE = '/home/veveo/CURATION_TOOL/LOGS/curation_authentication' 
log = init_log('authentication', LOG_FILE)


def login(request, username, password, data={}):
    log.info('login process started for %s' % username)
    user = authenticate(username=username, password=password)
    if not user:
        log.debug('login failed as no user exist with the given username and password')
        raise exceptions.InvalidUserNameOrPasswordError

    if not user.is_active:
        log.warning('login failed as user is not active')
        raise exceptions.AccountDisabledError
    
    django_login(request, user)
    result = {'success': True}
    log.info('login is successful')
    require_api_key = data.get('require_api_key', False)
    if require_api_key:
        result['apikey'] = _get_api_key(user)
    return result

'''
def signup(username, password, **kwargs):
    if not username or not password:
        raise exceptions.InvalidUserNameOrPasswordError
    if not len(password) < constanst.PASSWORD_MIN_LENGTH:
        raise exceptions.InvalidUserNameOrPasswordError
    defaults = {}
    user, created = User.objects.get_or_create(username=username, defaults=defaults)
    if not created:
        raise exceptions.UserAleadryExistsError
    user.set_password(password)
    return user
'''

def signup(username, password, data):
    log.info('signup process started for %s' % username)
    email = data.get('email', '').strip()
    require_api_key = data.get('require_api_key', False)
    valid_user, response = _can_user_signup(username)
    if not valid_user:
        return response
    result = {'success': True}

    user = _create_user(username, email=email, password=password)
    if require_api_key:
        result['apikey'] = _get_api_key(user)
    log.info('signup process completed successfully')
    return result


def get_all_users():
    """this function returns all users data """
    log.info('getting all users for analytics started')
    user_dict = {}
    users = User.objects.all()
    for user in users:
        _name = user.first_name + " "+ user.last_name
        user_dict.update({user.username: [user.id, _name, user.email]})
    log.info('getting all users for analytics ended')
    return user_dict


# Private
######################

def _get_api_key(user):
    try:
        return ApiKey.objects.get(user=user).key
    except ApiKey.DoesNotExist:
        api_key = ApiKey.objects.create(user=user)
        return api_key.key


def _is_username_email_present(username):
    if not username:
        return False, False
    username_present = User.objects.filter(username=username).count() != 0
    email_present = User.objects.filter(email=username).count() != 0
    return username_present, email_present


def _can_user_signup(username):
    if len(username) < 1:
        log.info('signup failed as username is too small')
        return False, exceptions.InvalidUserNameOrPasswordError
    username_present, email_present = _is_username_email_present(username)
    if username_present:
        log.info('signup failed as username is already present')
        return False, exceptions.UsernameAlreadyExistError
    if email_present:
        log.info('signup failed as email is already present')
        return False, exceptions.EmailAlreadyExistError
    return True, None


def _create_user(username, email=None, password=None, name=None, is_temp_user=False):

    log.info('creating user')
    if not email:
        email = username
    try:
        user = User.objects.create_user(
            username=username, email=email, password=password)
    except IntegrityError:
        log.error('user creation failed as username is already exist')
        raise exceptions.UserNameAlreadyExist
    return user



