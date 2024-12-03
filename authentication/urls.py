from django.urls import path
from .views import *

urlpatterns = [
    #path('', login_page, name='login'),
    path('login/',login_page,name='login'),
    path('register/',register_page,name='register'),
    path('', home,name='home'),
    path('logout/', logout_view,name='logout'),
]