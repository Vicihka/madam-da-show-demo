"""
WebSocket Consumers for Real-Time Order Updates
"""
import json
from channels.generic.websocket import AsyncWebsocketConsumer
from channels.db import database_sync_to_async
from .models import Order, OrderItem


class OrderConsumer(AsyncWebsocketConsumer):
    """WebSocket consumer for order updates"""
    
    async def connect(self):
        """Called when WebSocket connection is established"""
        # Join the 'orders_updates' group
        self.group_name = 'orders_updates'
        
        await self.channel_layer.group_add(
            self.group_name,
            self.channel_name
        )
        
        await self.accept()
        print(f"WebSocket connected: {self.channel_name}")
    
    async def disconnect(self, close_code):
        """Called when WebSocket connection is closed"""
        # Leave the 'orders_updates' group
        await self.channel_layer.group_discard(
            self.group_name,
            self.channel_name
        )
        print(f"WebSocket disconnected: {self.channel_name}")
    
    async def receive(self, text_data):
        """Called when message is received from WebSocket"""
        try:
            data = json.loads(text_data)
            message_type = data.get('type')
            
            if message_type == 'ping':
                # Respond to ping with pong
                await self.send(text_data=json.dumps({
                    'type': 'pong'
                }))
        except json.JSONDecodeError:
            pass
    
    # Handler for 'new_order' message type
    async def new_order(self, event):
        """Send new order notification to WebSocket"""
        await self.send(text_data=json.dumps({
            'type': 'new_order',
            'order': event['order']
        }))
    
    # Handler for 'status_changed' message type
    async def status_changed(self, event):
        """Send status change notification to WebSocket"""
        await self.send(text_data=json.dumps({
            'type': 'status_changed',
            'order': event['order'],
            'old_status': event.get('old_status'),
            'new_status': event.get('new_status')
        }))
    
    # Handler for 'payment_confirmed' message type
    async def payment_confirmed(self, event):
        """Send payment confirmation notification to WebSocket"""
        await self.send(text_data=json.dumps({
            'type': 'payment_confirmed',
            'order': event['order']
        }))

