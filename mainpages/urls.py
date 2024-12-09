
from django.urls import path
from .views import *

urlpatterns = [
    path('', createElection,name='election-create'),
   path('election-create/', createElection,name='election-create'),
]