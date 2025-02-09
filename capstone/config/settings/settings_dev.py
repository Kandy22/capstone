from .settings_base import *  # noqa

# SECURITY WARNING: keep the secret key used in production secret!
SECRET_KEY = 'k2#@_q=1$(__n7#(zax6#46fu)x=3&^lz&bwb8ol-_097k_rj5'

# nacl.encoding.Base64Encoder.encode(nacl.utils.random(nacl.secret.SecretBox.KEY_SIZE))
REDACTION_KEY = b'DPpSaf/iGNmq/3SYOPH6LfCZ9jUFkuoGKXycb2Of5Ms='

# SECURITY WARNING: don't run with debug turned on in production!
DEBUG = True

# don't check password quality locally, since it's annoying
AUTH_PASSWORD_VALIDATORS = []

# don't require celery listener
CELERY_TASK_ALWAYS_EAGER = True
# propagate exceptions
CELERY_TASK_EAGER_PROPAGATES = True

MAKE_HTTPS_URLS = False

if os.environ.get('DOCKERIZED'):
    DATABASES['default']['PASSWORD'] = 'password'
    DATABASES['default']['HOST'] = 'db'
    DATABASES['capdb']['PASSWORD'] = 'password'
    DATABASES['capdb']['HOST'] = 'db'
    DATABASES['user_data']['PASSWORD'] = 'password'
    DATABASES['user_data']['HOST'] = 'db'
    REDIS_HOST = 'redis'

    # this will only be used if CELERY_TASK_ALWAYS_EAGER = False
    CELERY_BROKER_URL = 'redis://redis'
    CELERY_RESULT_BACKEND = 'redis://redis'

    ELASTICSEARCH_DSL['default']['hosts'] = 'elasticsearch:9200'

# turn sql console logging on by setting DEBUG_SQL = True
DEBUG_SQL = False

if DEBUG_SQL:
    LOGGING['handlers']['sql'] = {
        'level': 'DEBUG',
        'class': 'logging.StreamHandler',
    }
    LOGGING['loggers']['django.db.backends'] = {
        'level': 'DEBUG',
        'handlers': ['sql']
    }

TEST_SLOW_QUERIES_DB_NAME = 'capstone_test_queries'
# to use slow queries db, add this to settings.py:
# DATABASES['default']['NAME'] = TEST_SLOW_QUERIES_DB_NAME

# don't update elasticsearch index on dev when savings cases (this may want to change -- not sure)
MAINTAIN_ELASTICSEARCH_INDEX = True

import sys
if 'pytest' not in sys.modules:
    ## settings not for tests

    # django-debug-toolbar
    try:
            import debug_toolbar  # noqa
            INSTALLED_APPS += (
                'debug_toolbar',
            )
            MIDDLEWARE.insert(
                MIDDLEWARE.index('django.contrib.sessions.middleware.SessionMiddleware'),
                'debug_toolbar.middleware.DebugToolbarMiddleware',
            )
            DEBUG_TOOLBAR_CONFIG = {
                'SHOW_TOOLBAR_CALLBACK': 'capweb.helpers.show_toolbar_callback'
            }
            INTERNAL_IPS = ['127.0.0.1']
    except ImportError:
        pass


# Print sent emails to the console, for debugging
EMAIL_BACKEND = 'django.core.mail.backends.console.EmailBackend'

# For testing error reporting
ADMINS = [('John', 'john@example.com'), ('Mary', 'mary@example.com')]

# Reveal 'draft' markdown documents
DOCS_SHOW_DRAFTS = True

# a list of labs projects to hide
LABS_HIDDEN = []