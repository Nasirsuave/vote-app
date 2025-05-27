from .views import *
from django.urls import path
from datetime import date


urlpatterns = [
    path('',notificationCreate,name='create-notification'),
    path('notify-user/<int:election_id>/<int:user_id>/',trigger_notification,name='notify-user'),
    
    ]

#user_id, message,read_at, created_at, is_read=False, election_id=None, election_name=None
