
from django.urls import path
from .views import *

urlpatterns = [
    #  path('', createElection,name='election-create'),
    #path('election-create/', createElection,name='election-create'),
    path('',election_list,name='election-list'),
    path('election-list/',election_list,name='election-list'),
    path('election-detail/<int:election_id>/',election_detail,name='election-detail'),
]