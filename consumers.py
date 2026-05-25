import json
from channels.generic.websocket import AsyncWebsocketConsumer

class ChatConsumer(AsyncWebsocketConsumer):
    async def connect(self):
        # Room ka ek farzi naam rakh lete hain
        self.room_name = "global_chat"
        self.room_group_name = f"chat_{self.room_name}"

        # Is user ko global group mein add karein
        await self.channel_layer.group_add(
            self.room_group_name,
            self.channel_name # Ab yeh layer enable hone ki wajah se error nahi dega
        )
        await self.accept()
        print("✅ User added to global chat room!")

    async def disconnect(self, close_code):
        # Disconnect hone par group se nikal dein
        await self.channel_layer.group_discard(
            self.room_group_name,
            self.channel_name
        )
        print("❌ User left the chat room")

    async def receive(self, text_data):
        data = json.loads(text_data)
        message = data.get('message', '')

        print(f"📩 Broadcaster received: {message}")

        # Poore group (room) ko message bhejein
        await self.channel_layer.group_send(
            self.room_group_name,
            {
                'type': 'chat_message',
                'message': message
            }
        )

    # Yeh function group_send ki taraf se chalaya jata hai
    async def chat_message(self, event):
        message = event['message']

        # Har client (user) ki screen par message send karein
        await self.send(text_data=json.dumps({
            'message': message
        }))
        print("📤 Message broadcasted to a user screen")