"""
Telegram Bot for Employee Order Management
Allows employees to manage orders directly from Telegram
"""
import requests
import json
from django.conf import settings
from django.utils import timezone
from .models import Order, OrderItem
from django.urls import reverse


def send_telegram_message(chat_id, text, reply_markup=None, parse_mode='HTML'):
    """Send message to Telegram"""
    try:
        bot_token = settings.TELEGRAM_BOT_TOKEN
        if not bot_token:
            return False
        
        url = f"https://api.telegram.org/bot{bot_token}/sendMessage"
        
        data = {
            'chat_id': chat_id,
            'text': text,
            'parse_mode': parse_mode
        }
        
        if reply_markup:
            data['reply_markup'] = json.dumps(reply_markup)
        
        response = requests.post(url, json=data, timeout=10)
        return response.status_code == 200
    except Exception as e:
        print(f"Error sending Telegram message: {e}")
        return False


def format_order_message(order, include_items=True):
    """Format order details for Telegram message"""
    try:
        items_text = ""
        if include_items:
            items = OrderItem.objects.filter(order=order)
            for item in items:
                items_text += f"  • {item.product_name} x{item.quantity} = ${item.subtotal}\n"
        
        status_emoji = {
            'pending': '⏳',
            'confirmed': '✅',
            'preparing': '👷',
            'ready_for_delivery': '📦',
            'out_for_delivery': '🚚',
            'delivered': '🎉',
            'cancelled': '❌'
        }
        
        payment_emoji = '💰' if order.payment_method == 'Cash on Delivery' else '💳'
        
        message = f"""📦 <b>Order #{order.order_number}</b>

{status_emoji.get(order.status, '📋')} Status: <b>{order.get_status_display()}</b>
{payment_emoji} Payment: <b>{order.payment_method}</b>

👤 <b>Customer:</b>
   Name: {order.customer_name}
   Phone: {order.customer_phone}
   Address: {order.customer_address}
   Province: {order.customer_province}

{items_text if items_text else ''}
💰 Total: <b>${order.total}</b>
⏰ Time: {order.created_at.strftime('%Y-%m-%d %H:%M')}
"""
        
        # Add COD payment status if applicable
        if order.payment_method == 'Cash on Delivery':
            if order.payment_received:
                message += "\n✅ Payment: <b>Received</b>"
            else:
                message += "\n⏳ Payment: <b>Pending</b>"
        
        return message
    except Exception as e:
        return f"Error formatting order: {str(e)}"


def create_order_keyboard(order):
    """Create inline keyboard for order actions"""
    keyboard = []
    
    # Status update buttons based on current status
    if order.status in ['pending', 'confirmed']:
        keyboard.append([{
            'text': '👷 Start Preparing',
            'callback_data': f'status_{order.order_number}_preparing'
        }])
    
    elif order.status == 'preparing':
        keyboard.append([{
            'text': '📦 Mark Ready',
            'callback_data': f'status_{order.order_number}_ready_for_delivery'
        }])
        
        # QR code button for COD orders
        if order.payment_method == 'Cash on Delivery' and not order.payment_received:
            keyboard.append([{
                'text': '🖨️ Get QR Code Link',
                'callback_data': f'qr_{order.order_number}'
            }])
    
    elif order.status == 'ready_for_delivery':
        keyboard.append([{
            'text': '🚚 Out for Delivery',
            'callback_data': f'status_{order.order_number}_out_for_delivery'
        }])
    
    elif order.status == 'out_for_delivery':
        keyboard.append([{
            'text': '✅ Mark Delivered',
            'callback_data': f'status_{order.order_number}_delivered'
        }])
    
    # Always show view details button
    keyboard.append([{
        'text': '📋 View Details',
        'url': f'http://127.0.0.1:8000/employee/order/{order.order_number}/'
    }])
    
    return {'inline_keyboard': keyboard}


def send_new_order_notification(order, employee_chat_ids=None):
    """Send new order notification to employees"""
    if not employee_chat_ids:
        # Default to admin chat if no employee IDs specified
        employee_chat_ids = [settings.TELEGRAM_CHAT_ID] if settings.TELEGRAM_CHAT_ID else []
    
    message = f"""🛒 <b>NEW ORDER RECEIVED!</b>

{format_order_message(order)}"""
    
    keyboard = create_order_keyboard(order)
    
    for chat_id in employee_chat_ids:
        send_telegram_message(chat_id, message, reply_markup=keyboard)


def handle_telegram_command(command, chat_id, message_text=None):
    """Handle Telegram bot commands"""
    command = command.lower().strip()
    
    if command == '/start' or command == '/help':
        help_text = """🤖 <b>MADAM DA Order Management Bot</b>

<b>Commands:</b>
/orders - View pending orders
/preparing - View orders being prepared
/ready - View orders ready for delivery
/out - View orders out for delivery
/order [NUMBER] - View specific order details

<b>Example:</b>
/order MD00001

<b>Quick Actions:</b>
Use buttons on order messages to update status instantly!
"""
        send_telegram_message(chat_id, help_text)
        return True
    
    elif command == '/orders':
        orders = Order.objects.filter(status__in=['pending', 'confirmed']).order_by('-created_at')[:10]
        if not orders:
            send_telegram_message(chat_id, "✅ No orders to prepare. All caught up!")
            return True
        
        send_telegram_message(chat_id, f"📋 <b>Orders to Prepare ({orders.count()})</b>")
        for order in orders:
            message = format_order_message(order, include_items=False)
            keyboard = create_order_keyboard(order)
            send_telegram_message(chat_id, message, reply_markup=keyboard)
        return True
    
    elif command == '/preparing':
        orders = Order.objects.filter(status='preparing').order_by('-created_at')[:10]
        if not orders:
            send_telegram_message(chat_id, "📦 No orders currently being prepared.")
            return True
        
        send_telegram_message(chat_id, f"👷 <b>Currently Preparing ({orders.count()})</b>")
        for order in orders:
            message = format_order_message(order, include_items=False)
            keyboard = create_order_keyboard(order)
            send_telegram_message(chat_id, message, reply_markup=keyboard)
        return True
    
    elif command == '/ready':
        orders = Order.objects.filter(status='ready_for_delivery').order_by('-created_at')[:10]
        if not orders:
            send_telegram_message(chat_id, "✅ No orders ready for delivery.")
            return True
        
        send_telegram_message(chat_id, f"📦 <b>Ready for Delivery ({orders.count()})</b>")
        for order in orders:
            message = format_order_message(order, include_items=False)
            keyboard = create_order_keyboard(order)
            send_telegram_message(chat_id, message, reply_markup=keyboard)
        return True
    
    elif command == '/out':
        orders = Order.objects.filter(status='out_for_delivery').order_by('-created_at')[:10]
        if not orders:
            send_telegram_message(chat_id, "🚚 No orders out for delivery.")
            return True
        
        send_telegram_message(chat_id, f"🚚 <b>Out for Delivery ({orders.count()})</b>")
        for order in orders:
            message = format_order_message(order, include_items=False)
            keyboard = create_order_keyboard(order)
            send_telegram_message(chat_id, message, reply_markup=keyboard)
        return True
    
    elif command.startswith('/order '):
        order_number = command.replace('/order ', '').strip().upper()
        try:
            order = Order.objects.get(order_number=order_number)
            message = format_order_message(order)
            keyboard = create_order_keyboard(order)
            send_telegram_message(chat_id, message, reply_markup=keyboard)
            return True
        except Order.DoesNotExist:
            send_telegram_message(chat_id, f"❌ Order {order_number} not found.")
            return True
    
    return False


def handle_callback_query(callback_data, chat_id, message_id):
    """Handle inline button callbacks"""
    try:
        if callback_data.startswith('status_'):
            # Format: status_ORDERNUMBER_NEWSTATUS
            parts = callback_data.split('_', 2)
            if len(parts) >= 3:
                order_number = parts[1]
                new_status = parts[2]
                
                try:
                    order = Order.objects.get(order_number=order_number)
                    old_status = order.status
                    order.status = new_status
                    order.save()
                    
                    # Send confirmation
                    status_names = {
                        'preparing': 'Preparing',
                        'ready_for_delivery': 'Ready for Delivery',
                        'out_for_delivery': 'Out for Delivery',
                        'delivered': 'Delivered'
                    }
                    
                    confirm_message = f"✅ Order #{order_number} status updated to <b>{status_names.get(new_status, new_status)}</b>"
                    send_telegram_message(chat_id, confirm_message)
                    
                    # Send updated order info
                    message = format_order_message(order)
                    keyboard = create_order_keyboard(order)
                    send_telegram_message(chat_id, message, reply_markup=keyboard)
                    
                    return True
                except Order.DoesNotExist:
                    send_telegram_message(chat_id, f"❌ Order {order_number} not found.")
                    return True
        
        elif callback_data.startswith('qr_'):
            # Format: qr_ORDERNUMBER
            order_number = callback_data.replace('qr_', '')
            try:
                order = Order.objects.get(order_number=order_number)
                
                if order.payment_method != 'Cash on Delivery':
                    send_telegram_message(chat_id, "❌ This order is not Cash on Delivery.")
                    return True
                
                # Generate QR code URL
                qr_url = f"http://127.0.0.1:8000/cod/print/{order_number}/"
                print_url = f"http://127.0.0.1:8000/cod/print/{order_number}/"
                
                message = f"""🖨️ <b>QR Code for Order #{order_number}</b>

📱 <b>Print Page:</b>
{print_url}

📋 <b>QR Code Image:</b>
http://127.0.0.1:8000/cod/qr/{order_number}/

💡 <b>Instructions:</b>
1. Open the print page link
2. Print the page (Ctrl+P)
3. Give to delivery driver

<b>Customer:</b> {order.customer_name}
<b>Total:</b> ${order.total}
"""
                send_telegram_message(chat_id, message)
                return True
            except Order.DoesNotExist:
                send_telegram_message(chat_id, f"❌ Order {order_number} not found.")
                return True
        
    except Exception as e:
        send_telegram_message(chat_id, f"❌ Error: {str(e)}")
        return False
    
    return False

