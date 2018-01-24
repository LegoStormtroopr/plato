#-*- coding: utf-8 -*-
"""
Django settings for aristotle_cloud with 12-factor settings

"""

import os
from decouple import config, Csv
from aristotle_mdr.required_settings import *

BASE_DIR = config(
    'aristotlemdr_BASE_DIR',
    os.path.join(os.path.dirname(os.path.dirname(__file__)), 'site')
)
STATIC_ROOT = config(
    'aristotlemdr_STATIC_DIR',
    default=os.path.join(BASE_DIR, "staticfiles")
)

# SECURITY WARNING: keep the secret key used in production secret!
import random, string
default_key = ''.join([
    random.SystemRandom().choice(
        "{}{}{}".format(string.ascii_letters, string.digits, string.punctuation))
    for i in range(50)
])
SECRET_KEY = config('SECRET_KEY', default=default_key)

# WSGI_APPLICATION = 'aristotle_cloud.env.wsgi.application'

# Database
# https://docs.djangoproject.com/en/1.10/ref/settings/#databases
import dj_database_url
DATABASE_URL = os.environ.get('DATABASE_URL', "sqlite:///%s/db.db"%(BASE_DIR))
DATABASES = {'default': dj_database_url.parse(DATABASE_URL)}


# Static files (CSS, JavaScript, Images)
STATIC_URL = "/static/"
# STATICFILES_STORAGE = 'whitenoise.storage.CompressedManifestStaticFilesStorage'
ROOT_URLCONF = 'dev.urls'


from urllib.parse import urlparse
es = (
    config('SEARCHBOX_URL', None) or
    config('BONSAI_URL', None)
)

if es is not None:
    es = urlparse(es)
    port = es.port or 80
    
    HAYSTACK_CONNECTIONS = {
        'default': {
            'ENGINE': 'haystack_elasticsearch.elasticsearch5.Elasticsearch5SearchEngine',
            'URL': es.scheme + '://' + es.hostname + ':' + str(port),
            'INDEX_NAME': 'documents',
        },
    }
    if es.username:
        HAYSTACK_CONNECTIONS['default']['KWARGS'] = {"http_auth": es.username + ':' + es.password}
else:
    HAYSTACK_CONNECTIONS = {
        'default': {
            'ENGINE': 'aristotle_mdr.contrib.search_backends.facetted_whoosh.FixedWhooshEngine',
            'PATH': os.path.join(os.path.dirname(__file__), 'whoosh_index'),
            'INCLUDE_SPELLING': True,
        },
    }

HAYSTACK_SIGNAL_PROCESSOR = 'aristotle_mdr.contrib.help.signals.AristotleHelpSignalProcessor'


# If DEBUG isn't *exactly* True, then its false. No 'truthiness' here.
DEBUG = config('aristotlemdr__DEBUG', default=False, cast=lambda s: s == "True")
debug_file = os.path.join(BASE_DIR,'logs/debug.log')

ALLOWED_HOSTS = config('ALLOWED_HOSTS', cast=Csv())


# PROFILING
###########################################
# INSTALLED_APPS += ('silk',)
# MIDDLEWARE_CLASSES = (
#     'silk.middleware.SilkyMiddleware',
# )+MIDDLEWARE_CLASSES
SILKY_PYTHON_PROFILER = True

SILKY_DYNAMIC_PROFILING = [{
    'module': 'aristotle_mdr.views.user_pages',
    'function': 'home'
}]

# ANYMAIL = {
#     "MAILGUN_API_KEY": config('MAILGUN_API_KEY', default="without a key emails won't send"),
# }
# EMAIL_BACKEND = "anymail.backends.mailgun.EmailBackend"
# DEFAULT_FROM_EMAIL = "account-recovery@mg.aristotlemetadata.com"


# if os.environ.get('django__NO_SIGNALS', None) == 'True' and \
#   os.environ.get('django__NO_SIGNALS', None) == 'True' and \
#   os.environ.get('django__NO_SIGNALS', None) == 'True':
#     from django.dispatch.dispatcher import Signal
    
#     def send(*args, **kwargs):
#         pass
#     def send_robust(*args, **kwargs):
#         pass
#     Signal.send = send
#     Signal.send_robust = send_robust

# INSTALLED_APPS += ('django_spaghetti',)

SPAGHETTI_SAUCE = {
    # 'apps':['aristotle_mdr','aristotle_dse','comet'],
    'apps': list(INSTALLED_APPS)+['auth'],
    'show_fields':False,
    'ignore_self_referential':True,
    'exclude':{
        # 'aristotle_mdr':[
        #     '_concept',
        #     'workgroup',
        #     'supplementaryvalue',
        #     'registrationauthority',
        #     'organization',
        #     'status',
        #     'reviewrequest',
        #     'possumprofile',
        #     'discussionpost',
        #     'discussioncomment',
        # ],
        # 'aristotle_dse': [
        #     'dssdeinclusion',
        #     'dssclusterinclusion',
        #     'datasource'
        # ],
        # 'comet': [
        #     'qualitystatement',
        #     'indicatorsettype'
        # ]
    }
}