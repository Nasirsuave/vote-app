# notification/routing.py

from django.urls import re_path # Using re_path for more flexibility, or you can use path
from . import consumers # Import your consumers module

websocket_urlpatterns = [
    # This path matches the URL for your WebSocket connection.
    # It sends all WebSocket traffic on 'ws/notify/' to the NotificationConsumer.
    # The user information will be available in the consumer via self.scope["user"]
    # because you wrapped your URLRouter in AuthMiddlewareStack in asgi.py.
    re_path(r'ws/notify/$', consumers.NotificationConsumer.as_asgi()),
]