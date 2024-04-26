import json
from asgiref.sync import async_to_sync
from channels.generic.websocket import WebsocketConsumer
from .models import Chats
from datetime import datetime
import jwt
from django.conf import settings
from .models import Chats
from django.http import QueryDict

class ChatConsumer(WebsocketConsumer):
    def connect(self):
        print("CONNECTING....")

        query_string = self.scope['query_string'].decode("utf8")
        query_dict = QueryDict(query_string)
        token = query_dict.get('token')
        recipient_id = int(query_dict.get('recipient'))
        user = self.authenticate_token(token)

        if user:
            self.scope["user"] = user
            self.room_name = self.generate_room_name(user.id, recipient_id)
            async_to_sync(self.channel_layer.group_add)(self.room_name, self.channel_name)
            self.accept()
        else:
            self.close()

    def disconnect(self, code):
        # Leave room group
        async_to_sync(self.channel_layer.group_discard)(
            self.room_name, self.channel_name
        )

    def receive(self, text_data):
        print("Received Called")

        data = json.loads(text_data)
        message = data['message']
        sender_id = self.scope["user"].id
        recipient_id = data['recipientId']

        new_message = Chats.objects.create(
            sender_id=sender_id,
            recipient_id=recipient_id,
            message=message,
            sent_at=datetime.now()
        )
        
        # Send message to room group
        async_to_sync(self.channel_layer.group_send)(
            self.room_name, 
            {
                "type": "chat_message", 
                "message": message,
                "sender": sender_id,
                "recipient": recipient_id
            }
        )
    
    def chat_message(self, event):
        print("Chat Message Called")
        message = event['message']
        sender_id = event['sender']
        recipient_id = event['recipient']
        
        # Send message to WebSocket
        self.send(text_data=json.dumps({"message": message, "sender_id": sender_id, "recipient_id": recipient_id  }))


    def authenticate_token(self, token):
        try:
            decoded_token = jwt.decode(token, settings.SECRET_KEY, algorithms=['HS256'])
            user_id = decoded_token['user_id']
            return self.get_user(user_id)
        except jwt.ExpiredSignatureError:
            return None
        except jwt.InvalidTokenError:
            return None
        
    def get_user(self, userId):
        try:
            return Chats.objects.get(id=userId)
        except:
            return None 
        
    def generate_room_name(self, user1, user2):
        sorted_users = sorted([user1, user2])
        return f"chat_{sorted_users[0]}_{sorted_users[1]}"