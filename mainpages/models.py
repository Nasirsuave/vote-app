from django.db import models
from django.contrib.auth.models import User

class Election(models.Model):
    title = models.CharField(max_length=255)  # Add max_length for CharField
    description = models.TextField()
    start_date = models.DateField()
    end_date = models.DateField()

    def __str__(self):
        return f"{self.id} {self.title} {self.description} {self.start_date} {self.end_date}"


class Candidate(models.Model):
    name = models.CharField(max_length=255)
    election = models.ForeignKey(Election, on_delete=models.CASCADE, related_name="candidates")

    def __str__(self):
        return self.name


class Vote(models.Model):
    user = models.ForeignKey(User, on_delete=models.CASCADE, related_name="votes") #many votes can be associated with a single user.
    election = models.ForeignKey(Election, on_delete=models.CASCADE, related_name="votes") #many votes can belong to a single election.
    candidate = models.ForeignKey(Candidate, on_delete=models.CASCADE, related_name="votes") #many votes can be cast for a single candidate.
    vote = models.BooleanField(default=False)  # Optional: mark if the vote was successful

    class Meta:
        unique_together = ('user', 'election')  # Ensures a user can only vote once per election

    def __str__(self):
        return f"{self.user} voted for {self.candidate} in {self.election}"


class VoterEligibility(models.Model):
    user = models.ForeignKey(User, on_delete=models.CASCADE, related_name="eligibilities") #user with more election he's eligible to
    election = models.ForeignKey(Election, on_delete=models.CASCADE, related_name="eligible_voters")

    class Meta:
        unique_together = ('user', 'election') # Ensures no duplicate entries for the same user and election
        
        def __str__(self):
            return f"{self.user.username} eligible for {self.election.title}"