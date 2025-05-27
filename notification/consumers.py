import json
from channels.generic.websocket import AsyncWebsocketConsumer
from channels.db import database_sync_to_async #To handle sync database operations in async consumers
from .views import save_notification_to_db

class NotificationConsumer(AsyncWebsocketConsumer):
    async def connect(self):
        print("Connect message called")
        self.user = self.scope["user"] #Get the user object
        if self.user.is_anonymous:
             print("Not authenticated")
             await self.close()
             
        else:
            self.room_group_name = f'user_{self.user.id}'  # Unique group name for the user
            print("Authenticated")
            print(f"user Id : {self.user.id}")
            await self.channel_layer.group_add(
                self.room_group_name,
                self.channel_name
            )
            await self.accept()
            print("Connection Established!")

    async def disconnect(self, close_code):
        await self.channel_layer.group_discard(
            self.room_group_name,
            self.channel_name
        )

    async def receive(self, text_data):
        text_data_json = json.loads(text_data) # convert notification received from client to python dicitionary
        message = text_data_json['message']  # gets only the message value 
        # Send message to group (and thus to all connected clients)
        await self.channel_layer.group_send(
            self.room_group_name,  #send to the user specific group
            {
                'type': 'notification.message',  # Custom type for handling notification messages
                'message': message,
            }
        )

        #call save_notification_to_db here 
        



    # Handler for the custom message type
    async def notification_message(self, event):
        #message = event['message']
        # Send message to WebSocket

        await self.send(text_data=json.dumps({
            'event': event,
        }))

        

    
    