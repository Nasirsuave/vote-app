from django.shortcuts import render

# Create your views here.

def createElection(request):
    return render(request,'mainpages/create_election.html')

