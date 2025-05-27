from django.contrib import admin

# Register your models here.
from django.contrib import admin
from .models import UserNotification


class UserNotificationAdmin(admin.ModelAdmin):
    list_display = ("user_id","message","election_id","election_name","is_read","created_at","read_at")

    def user_id(self,User):
        return User.user.id
# Register your models here.

admin.site.register(UserNotification,UserNotificationAdmin)
