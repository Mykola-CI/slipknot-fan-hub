#!/usr/bin/env python

import os
import sys
from project_fandom.settings import base


def main():
    """Run administrative tasks.
    DEBUG is set to True by default in .env file.
    In production DEBUG must be added to Heroku Config Vars and set to False.
    """

    if base.DEBUG:
        os.environ.setdefault("DJANGO_SETTINGS_MODULE",
                              "project_fandom.settings.local")
    else:
        os.environ.setdefault("DJANGO_SETTINGS_MODULE",
                              "project_fandom.settings.production")

    try:
        from django.core.management import execute_from_command_line
    except ImportError as exc:
        raise ImportError(
            "Couldn't import Django. Are you sure it's installed and "
            "available on your PYTHONPATH environment variable? Did you "
            "forget to activate a virtual environment?"
        ) from exc
    execute_from_command_line(sys.argv)


if __name__ == "__main__":
    main()
