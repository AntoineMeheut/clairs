"""
ASGI config for backend project.

It exposes the ASGI callable as a module-level variable named ``application``.

For more information on this file, see
https://docs.djangoproject.com/en/5.0/howto/deployment/asgi/
"""

import os

from channels.auth import AuthMiddlewareStack
from channels.routing import ProtocolTypeRouter, URLRouter
from channels.security.websocket import AllowedHostsOriginValidator
from django.core.asgi import get_asgi_application

# Follows the path of cookiecutter-django
os.environ.setdefault("DJANGO_SETTINGS_MODULE", "config.settings")
os.environ.setdefault("DJANGO_ADMIN_SHELLX_SUPERUSER_ONLY", "True")
os.environ.setdefault("DJANGO_ADMIN_SHELLX_COMMANDS", "/bin/bash")
os.environ.setdefault("DJANGO_SETTINGS_MODULE", "80")

# The ASGI application
django_application = get_asgi_application()

# Remember to import the urlpatters after the asgi application!
# pylint: disable=wrong-import-position
from django_admin_shellx.urls import websocket_urlpatterns

application = ProtocolTypeRouter(
    {
        "websocket": AllowedHostsOriginValidator(
            AuthMiddlewareStack(URLRouter(websocket_urlpatterns))
        ),
    }
)
