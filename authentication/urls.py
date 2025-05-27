from django.urls import path
from .views import *
from mainpages.views import createElection,checkResult
from notification.views import notificationCreate

urlpatterns = [
    #path('',login_page,name='login'),
    path('',home,name='home'),
    #path('election-create/', createElection,name='election-create'),
    path('home/',home,name='home'),
    path('login/',login_page,name='login'),
    path('register/',register_page,name='register'),
    path('logout/', logout_view,name='logout'),
    path('election-create',createElection,name='election-create'),
    path('election-result',checkResult,name='election-result'),
    path('notification-create',notificationCreate,name='notification-create'),
]