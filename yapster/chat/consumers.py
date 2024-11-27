import json
from channels.generic.websocket import AsyncWebsocketConsumer
from channels.db import database_sync_to_async
from chat.models import *
class ChatConsumer(AsyncWebsocketConsumer):        
    async def connect(self):
        self.chat_name = f"room_{self.scope['url_route']['kwargs']['chat_name']}"
        await self.channel_layer.group_add(self.chat_name, self.channel_name)
        await self.accept()
        
    async def disconnect(self, close_code):
        await self.channel_layer.group_discard(self.chat_name, self.channel_name)
        
    # When the socket.send() method is called, the WebSocket connection transmits the message to the server.
    # The receive method is automatically triggered to handle the incoming message.
    async def receive(self, text_data):
        text_data_json = json.loads(text_data)
        data = text_data_json
        await self.create_message(data=data)
        # Trigger send_message method
        await self.channel_layer.group_send(
            self.chat_name,
            {
                'type': 'send_message',
                'data': data,
            }
        )
    async def send_message(self, event):
        data = event['data']
        print(data)
        # await self.create_message(data=data)
        # response_data = {
        #     'sender': data['sender'],
        #     'message': data['message']
        # }
        await self.send(text_data=json.dumps({"response_data" : data}))
        
    # This decorator is part of Django Channels and is used to allowsynchronous database 
    # operations to be called from asynchronous code (like your WebSocket consumers).
    @database_sync_to_async 
    def create_message(self, data):
        try:
            # Get the chat room by name
            chat = Chat.objects.get(chat_name=data['chat_name'])
            
            # Get the sender User instance
            sender = User.objects.get(username=data['sender'])
            
            # Check for duplicates based on chat, sender, and content
            # if not Message.objects.filter(content=data['message'], chat=chat, sender=sender).exists():
            new_message = Message(
                chat=chat,
                sender=sender,
                content=data['message']
            )
            new_message.save()
            print(1)
            return {"success": True, "message": "Message saved successfully."}
        except Chat.DoesNotExist:
            print(2)
            return {"success": False, "message": "Chat room does not exist."}
        except User.DoesNotExist:
            print(3)
            return {"success": False, "message": "Sender does not exist."}
        except Exception as e:
            print(4)
            return {"success": False, "message": str(e)}