# """
# ASGI config for my_vote_system project.

# It exposes the ASGI callable as a module-level variable named ``application``.

# For more information on this file, see
# https://docs.djangoproject.com/en/5.1/howto/deployment/asgi/
# """
# import django
# import os

# from django.core.asgi import get_asgi_application
# from channels.routing import ProtocolTypeRouter, URLRouter
# from channels.auth import AuthMiddlewareStack #Important for authentication
# from notification import consumers
# from django.urls import path
# from notification import routings



# os.environ.setdefault('DJANGO_SETTINGS_MODULE', 'my_vote_system.settings')
# django.setup()


# application = ProtocolTypeRouter({
#     "http": get_asgi_application(), #HTTP requests
#     "websocket": AuthMiddlewareStack(URLRouter([ # WebSocket requests
#          #path('ws/notify/', consumers.NotificationConsumer.as_asgi()),  # Define your WebSocket routing here, inside URLRouter
#          routings.websocket_urlpatterns
#     ])),
# })



###NEW

# my_vote_system/my_vote_system/asgi.py

import os
import django # Keep this import at the top

# --- Step 1: Set the Django settings module environment variable ---
os.environ.setdefault('DJANGO_SETTINGS_MODULE', 'my_vote_system.settings')

# --- Step 2: Call django.setup() to initialize Django's settings and app registry ---
django.setup() # <--- THIS IS THE CRUCIAL PLACEMENT

# --- Step 3: Now, safely import modules that depend on Django's configuration ---
# (These imports will now happen AFTER Django's settings are loaded)
from django.core.asgi import get_asgi_application
from channels.routing import ProtocolTypeRouter, URLRouter
from channels.auth import AuthMiddlewareStack

# Import your application's routing here
from notification import routings # This imports your notification/routings.py
# You generally don't need to import 'consumers' directly here if it's handled by your routing.py
# from notification import consumers # You can remove this line if it's only imported via routings.py

# The `path` import is typically not needed in asgi.py unless you're defining paths directly here
# from django.urls import path


application = ProtocolTypeRouter({
    "http": get_asgi_application(), # Handle standard HTTP requests
    "websocket": AuthMiddlewareStack( # Apply authentication middleware for WebSockets
        URLRouter(
            routings.websocket_urlpatterns # Use the WebSocket URL patterns defined in notification/routings.py
        )
    ),
})