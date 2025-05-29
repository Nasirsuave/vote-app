from django.shortcuts import render
from channels.layers import get_channel_layer
from asgiref.sync import async_to_sync,sync_to_async
from channels.db import database_sync_to_async
from .models import UserNotification
from django.contrib.auth.models import User
import json
from django.utils import timezone
import datetime


def format_time_ago_python(created_at_dt):
    """
    Formats a datetime object into a "time ago" string.
    """

    # Step 1: Ensure created_at_dt is timezone-aware
    # In our example, created_at_dt (from DB) is already timezone-aware (<UTC>)
    # So, this 'if' condition will be False.
    if timezone.is_naive(created_at_dt):
        #DEBUG: created_at_dt was naive, making it aware to UTC.
        created_at_dt = timezone.make_aware(created_at_dt, timezone.utc)
    else:
        print(f"DEBUG: created_at_dt is already timezone-aware.")
    print(f"After timezone check, created_at_dt: {created_at_dt}")


    # Step 2: Get the current timezone-aware time
    now = timezone.now()
    #\nStep 2: Getting current time.
    #Current time (now): {now}
    #Type of now: {type(now)}


    # Step 3: Calculate the difference (timedelta object)
    diff = now - created_at_dt
    #\nStep 3: Calculating time difference.
    #Difference (timedelta object): {diff}
    # Example Calculation:
    #   (2025, 5, 27, 17, 39, 27, ...) - (2025, 5, 27, 17, 28, 47, ...)
    #   = 0 days, 0 hours, 10 minutes, 40 seconds
    #   (plus microseconds, if any)


    # Step 4: Convert timedelta to total seconds
    total_seconds = diff.total_seconds()
    #\nStep 4: Converting difference to total seconds.
    #Total seconds: {total_seconds}
    # Example: 10 minutes * 60 seconds/minute + 40 seconds = 600 + 40 = 640 seconds
    # So, total_seconds will be approximately 640.0 (or 640.something if microseconds are involved)


    # Step 5: Calculate differences in various units (and round)
    diff_minutes = round(total_seconds / 60)
    #\nStep 5a: Calculating difference in minutes.
    #Raw minutes: {total_seconds / 60}
    #Rounded diff_minutes: {diff_minutes}
    # Example: round(640.0 / 60) = round(10.666...) = 11

    diff_hours = round(total_seconds / (60 * 60))
    #Step 5b: Calculating difference in hours.
    #Raw hours: {total_seconds / 3600}
    #Rounded diff_hours: {diff_hours}
    # Example: round(640.0 / 3600) = round(0.177...) = 0

    diff_days = round(total_seconds / (60 * 60 * 24))
    #Step 5c: Calculating difference in days.
    #Raw days: {total_seconds / 86400}
    #Rounded diff_days: {diff_days}
    # Example: round(640.0 / 86400) = round(0.007...) = 0


    # Step 6: Apply conditional logic to return the appropriate string.
    #\nStep 6: Applying conditional logic.
    if diff_minutes < 1:
        #Condition: diff_minutes ({diff_minutes}) < 1 is FALSE.
        # Example: 11 < 1 is False.
        result = "Just now"
        return result

    elif diff_minutes < 60:
        #Condition: diff_minutes ({diff_minutes}) < 60 is TRUE.
        # Example: 11 < 60 is True. This condition is met!

        plural_s = 's' if diff_minutes != 1 else ''
        #Plural 's' for minutes: '{plural_s}'
        # Example: 's' because 11 is not 1.

        result = f"{diff_minutes} minute{plural_s} ago"
        #Returning: '{result}'
        return result
        # Function exits here.
    
    # The following conditions will NOT be evaluated because the 'elif diff_minutes < 60' was True.
    elif diff_hours < 24:
        #Condition: diff_hours ({diff_hours}) < 24 would be checked next (but won't be).
        plural_s = 's' if diff_hours != 1 else ''
        return f"{diff_hours} hour{plural_s} ago"
    elif diff_days < 7:
        #Condition: diff_days ({diff_days}) < 7 would be checked next (but won't be).
        plural_s = 's' if diff_days != 1 else ''
        return f"{diff_days} day{plural_s} ago"
    else:
        #"Condition: Fallback to full date would be checked next (but won't be).
        return created_at_dt.strftime("%b %d, %Y")



def notificationCreate(request):
    # all_notifs = UserNotification.objects.filter(user=request.user).order_by('-created_at')
    

    # for notif in all_notifs:
    # created_at = UserNotification.objects.filter(user=request.user).values('created_at')                                 #format_time_ago_python()
    # datetime.fromisoformat()         will use later

    all_notifications_for_template = []
    if request.user.is_authenticated:
        user_notifications_qs = UserNotification.objects.filter(
            user=request.user
        ).order_by('-created_at')

        for notif in user_notifications_qs:
            formatted_time_ago = format_time_ago_python(notif.created_at)
            notification_data = {
                'id': notif.id,
                'message': notif.message,
                'electionId': notif.election_id,
                'election_name': notif.election_name,
                'is_read': notif.is_read,
                'created_at_humanized': formatted_time_ago,
            }
            all_notifications_for_template.append(notification_data)

 
    return render(request,'notification/notification-page.html',{ "all_notifications_for_template": all_notifications_for_template})



async def trigger_notification(electionId,electionTitle,userId):
    notification_message_content = f"You have been added to election with ID : {electionId}"

    
    # Call your save_notification_to_db function here using await
    # Remember, save_notification_to_db is already @database_sync_to_async, so it's awaitable.
    # Pass the appropriate parameters. Note: 'created_at' is handled by auto_now_add in the model.
    saved_notification_info = await save_notification_to_db(
        user_id=userId,
        message=notification_message_content,
        election_id=electionId,
        election_name=electionTitle,
        # is_read and read_at have defaults in save_notification_to_db, so no need to pass # default
    )
    saved_notification_id = saved_notification_info["user_notification_id"]
    saved_notification_created_at = saved_notification_info["created_at"]

    print(f"saved_notification_id: {saved_notification_id}")
    print(f"saved_notification_created_at: {saved_notification_created_at}")

    if saved_notification_id: # Check if the notification was saved successfully (e.g., returns ID)
      print("Entered the if block")
      channel_layer = get_channel_layer()
        
        #send notification via the channel layer
      await channel_layer.group_send(
                        f"user_{userId}",  # Replace with the user's group name.  Use the same group name in the consumer
                        {
                            "type": "notification.message",  # Must match the 'type' in your consumer.py but the period can indicate underscore
                            "message": notification_message_content,
                            "electionId": electionId,
                            "userId": userId,
                            "election_name": electionTitle,
                            "created_at": saved_notification_created_at,
                        }
                    )
        
    
    # save_notification_to_db(userId,f"You have been added to election with ID : {electionId}",timezone.now(),election_id=electionId,election_name=electionTitle,)
    print("Notification function called!!")
    # return HttpResponse("Notification sent!")
    
@database_sync_to_async
def save_notification_to_db(user_id, message,is_read=False, election_id=None, election_name=None,read_at=None):
    try:
        user = User.objects.get(id=user_id) # Get the user object by ID
        user_notification = UserNotification.objects.create(
            user=user,
            message=message,
            election_id=election_id,
            election_name=election_name,
            is_read=is_read, # New notifications are unread by default
            read_at=read_at,
            # created_at is automatically set by auto_now_add=True
        )  
        #return user_notification.id
        return {"user_notification_id": user_notification.id,
                "created_at"  : user_notification.created_at.isoformat() #removed the 'Z' string we concatenated earlier
            }
    
    except Exception as e:
        print(f"Error saving notification to DB: {e}")



def notification_list(request):
    pass
