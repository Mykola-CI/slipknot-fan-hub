# Settings for production environment

import os
from .base import *

ALLOWED_HOSTS = [
    '.herokuapp.com'
]

STATIC_ROOT = os.path.join(BASE_DIR, 'staticfiles')
