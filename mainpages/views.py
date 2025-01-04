from django.shortcuts import render,redirect
from django.http import JsonResponse
from django.contrib import messages
from .models import Election,Candidate,Vote,VoterEligibility
from django.contrib.auth.models import User
import csv
from django.utils import timezone
from django.shortcuts import get_object_or_404
from django.db.models import Count
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


def election_list(request):
    # print("User id : ",request.user.id)
    print(VoterEligibility.objects.filter(
    #    user=request.user.id,
        election__start_date__lte=timezone.now(), 
        election__end_date__gt=timezone.now()
    )
)
    return VoterEligibility.objects.filter(
        user=request.user.id,
        election__start_date__lte=timezone.now(), 
        election__end_date__gt=timezone.now()
    )


def election_detail(request,election_id):
    election = get_object_or_404(Election,pk=election_id)
    election_candidates = Candidate.objects.filter(election=election_id)

    return render(request,
                  'mainpages/election_detail.html',
                  {'election':election,'election_candidates':election_candidates}
                  )


def cast_vote(request,election_id):
    if request.method == 'POST':
        candidate_id = request.POST.get('candidates')
        print(f"Candidate ID from POST: {candidate_id}")
        
        current_election =  get_object_or_404(Election,pk=election_id)
        print(f"Current Election ID from POST: {election_id}")

        candidate = get_object_or_404(Candidate, pk=candidate_id)

        Vote.objects.create(
              candidate=candidate,
              user=request.user,
              election = current_election,
              vote = True
        )

        # messages.info(request,f'Dear {request.user.username},your vote has been recorded')
        # return redirect(reverse('mainpages/election-detail', args=[election_id]))

        return JsonResponse({'message': '✅Your vote has been recorded successfully!'})
    # return render(request,'mainpages/election_detail.html')
    return JsonResponse({'error': 'Invalid request'}, status=400)


def checkResult(request):
    return render(request,'mainpages/check_result.html')



def displayResult(request):
    if request.method == "POST":
        electionId = request.POST.get('electionId')
        
        ready_display = VoterEligibility.objects.filter(
            election=electionId,
            user=request.user.id,
            election__end_date__lt=timezone.now()
            ).exists()
    
        election_candidates = Candidate.objects.filter(election=electionId)
        total_cast = Vote.objects.filter(election=electionId).count()
        each_total_vote = Vote.objects.filter(election=electionId).values('candidate__id').annotate(total_count=Count('candidate__id'))
    
        if ready_display:
            election_candidates_list = [
                {
                   'name': candidate.name,
                   'total_vote':next(
                                (vote['total_count'] for vote in each_total_vote if vote['candidate__id'] == candidate.id),0
                                    )
                }
                for candidate in election_candidates
           ]
            

            return JsonResponse({
                'election_candidates':election_candidates_list,
                # 'candidates_total':each_candidates_list,
                # 'total_cast':total_cast
            })
        elif not ready_display:
            return JsonResponse({'election_candidates': []})
        
    return JsonResponse({'error': 'Invalid request'}, status=400)

