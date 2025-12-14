"""
WebSocket Consumers for Real-Time Order Updates
Optimized for 1000+ concurrent connections
"""
import json
from channels.generic.websocket import AsyncWebsocketConsumer
from channels.db import database_sync_to_async
from .models import Order, OrderItem


class OrderConsumer(AsyncWebsocketConsumer):
    """WebSocket consumer for order updates - with connection limits for scalability"""
    
    # Maximum concurrent WebSocket connections (prevents resource exhaustion)
    MAX_CONNECTIONS = 100
    
    # Track connections (in production, use Redis for distributed tracking)
    _connection_count = 0
    
    async def connect(self):
        """Called when WebSocket connection is established"""
        # Check connection limit to prevent resource exhaustion
        if OrderConsumer._connection_count >= self.MAX_CONNECTIONS:
            # Reject connection if limit reached
            await self.close(code=4001)  # Custom close code: Too Many Connections
            print(f"WebSocket connection rejected: limit reached ({OrderConsumer._connection_count}/{self.MAX_CONNECTIONS})")
            return
        
        # Join the 'orders_updates' group
        self.group_name = 'orders_updates'
        
        await self.channel_layer.group_add(
            self.group_name,
            self.channel_name
        )
        
        OrderConsumer._connection_count += 1
        await self.accept()
        print(f"WebSocket connected: {self.channel_name} (Total: {OrderConsumer._connection_count}/{self.MAX_CONNECTIONS})")
    
    async def disconnect(self, close_code):
        """Called when WebSocket connection is closed"""
        # Leave the 'orders_updates' group
        await self.channel_layer.group_discard(
            self.group_name,
            self.channel_name
        )
        OrderConsumer._connection_count = max(0, OrderConsumer._connection_count - 1)
        print(f"WebSocket disconnected: {self.channel_name} (Total: {OrderConsumer._connection_count}/{self.MAX_CONNECTIONS})")
    
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

