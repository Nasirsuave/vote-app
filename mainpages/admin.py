from django.contrib import admin

# Register your models here.

from django.contrib import admin
from .models import Election,Candidate,Vote,VoterEligibility

class ElectionAdmin(admin.ModelAdmin):
      list_display = ("id","title", "description", "start_date","end_date",)


class CandidateAdmin(admin.ModelAdmin):
      list_display = ("id","name","election_id",)

      def election_id(self,Candidate):
            return Candidate.election.id
      

class VoterEligibilityAdmin(admin.ModelAdmin):
      list_display = ("user_id","election_id")

      def user_id(self,User):
            return User.user.id
      
      def election_id(self,Election):
            return Election.election.id

# Register your models here.
admin.site.register(Election,ElectionAdmin)
admin.site.register(Candidate,CandidateAdmin)
admin.site.register(Vote)
admin.site.register(VoterEligibility,VoterEligibilityAdmin)


