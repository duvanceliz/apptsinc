"""
WSGI config for apptsinc project.

It exposes the WSGI callable as a module-level variable named ``application``.

For more information on this file, see
https://docs.djangoproject.com/en/5.0/howto/deployment/wsgi/
"""

import os
import logging


from django.core.wsgi import get_wsgi_application

os.environ.setdefault('DJANGO_SETTINGS_MODULE', 'apptsinc.settings')

application = get_wsgi_application()

logging.basicConfig(
    filename='waitress.log',  # El archivo donde se almacenarán los logs
    level=logging.DEBUG,
    format='%(asctime)s %(levelname)s %(message)s',
)


# logging.basicConfig(level=logging.DEBUG)

