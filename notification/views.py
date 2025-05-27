from django.shortcuts import render
from channels.layers import get_channel_layer
from asgiref.sync import async_to_sync,sync_to_async
from channels.db import database_sync_to_async
from .models import UserNotification
from django.contrib.auth.models import User
import json
from django.utils import timezone


def notificationCreate(request):
    return render(request,'notification/notification-page.html')



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


