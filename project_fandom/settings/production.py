# Settings for production environment
from .base import *

ALLOWED_HOSTS = ['.herokuapp.com']

SITE_ID = 2

# For better compression and Cache management
STATICFILES_STORAGE = 'whitenoise.storage.CompressedManifestStaticFilesStorage'

