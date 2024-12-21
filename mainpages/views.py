from django.shortcuts import render
from django.contrib import messages
from .models import Election,Candidate,Vote,VoterEligibility
from django.contrib.auth.models import User
import csv


# Create your views here.

def createElection(request):
    if request.method == "POST":
        title = request.POST.get("title")
        description = request.POST.get("description")
        start_date = request.POST.get("start_date")
        end_date = request.POST.get("end_date")
        
        # Save to the database (if valid)
        election = Election.objects.create(
            title=title,
            description=description,
            start_date=start_date,
            end_date=end_date
        )

        total_candidates = int(request.POST.get("total_candidates"))
        for i in range(1, total_candidates + 1):
            candidate_name = request.POST.get(f"candidate_{i}")
            Candidate.objects.create(
                    name = candidate_name,
                    election = election
                )
        
        csv_file = request.FILES.get('file')
        if csv_file.name.endswith('.csv'):
            reader = csv.reader(csv_file.read().decode('utf-8').splitlines())
            for row in reader:
                username = row[0].strip()
                try:
                    user = User.objects.get(username=username)
                    VoterEligibility.objects.get_or_create(election=election,user=user)
                except Exception as UserNotFound:
                    continue



        
        #messages.info(request, "Election created Successfully!")


    return render(request,'mainpages/create_election.html')


