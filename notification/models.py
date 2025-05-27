from django.db import models
# notification/models.py
from django.db import models
from django.conf import settings # To get the User model
from django.utils import timezone

class UserNotification(models.Model):
    user = models.ForeignKey(settings.AUTH_USER_MODEL, on_delete=models.CASCADE, related_name='notifications')
    message = models.TextField()
    election_id = models.IntegerField(null=True, blank=True) # To link to the specific election
    election_name = models.CharField(max_length=255, null=True, blank=True)
    is_read = models.BooleanField(default=False)
    created_at = models.DateTimeField(auto_now_add=True) #When a UserNotification object is first created and saved to the database, Django will automatically fill in the created_at field with the current date and time.
    read_at = models.DateTimeField(null=True, blank=True)

    class Meta:
        ordering = ['-created_at'] # Order by newest first

    def __str__(self):
        return f"Notification for {self.user.username}: {self.message[:50]}..."
# Create your models here.
