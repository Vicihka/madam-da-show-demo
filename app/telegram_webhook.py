"""
Telegram Webhook Handler for Employee Bot
Processes incoming messages and callbacks from Telegram
"""
from django.http import JsonResponse, HttpResponse
from django.views.decorators.csrf import csrf_exempt
from django.views.decorators.http import require_http_methods
from django.conf import settings
import json
from .telegram_bot import handle_telegram_command, handle_callback_query


@csrf_exempt
@require_http_methods(["POST"])
def telegram_webhook(request):
    """Handle incoming Telegram webhook updates"""
    try:
        data = json.loads(request.body)
        
        # Handle message
        if 'message' in data:
            message = data['message']
            chat_id = message.get('chat', {}).get('id')
            text = message.get('text', '')
            
            if text.startswith('/'):
                # It's a command
                handle_telegram_command(text, chat_id)
        
        # Handle callback query (button clicks)
        elif 'callback_query' in data:
            callback = data['callback_query']
            chat_id = callback.get('message', {}).get('chat', {}).get('id')
            message_id = callback.get('message', {}).get('message_id')
            callback_data = callback.get('data', '')
            
            handle_callback_query(callback_data, chat_id, message_id)
            
            # Answer callback query to remove loading state
            try:
                import requests
                bot_token = settings.TELEGRAM_BOT_TOKEN
                callback_id = callback.get('id')
                url = f"https://api.telegram.org/bot{bot_token}/answerCallbackQuery"
                requests.post(url, json={
                    'callback_query_id': callback_id
                }, timeout=5)
            except:
                pass
        
        return JsonResponse({'ok': True})
        
    except Exception as e:
        print(f"Error processing webhook: {e}")
        return JsonResponse({'ok': False, 'error': str(e)}, status=500)


@require_http_methods(["GET", "POST"])
def set_telegram_webhook(request):
    """Set Telegram webhook URL"""
    try:
        import requests
        from django.conf import settings
        
        bot_token = settings.TELEGRAM_BOT_TOKEN
        if not bot_token:
            return JsonResponse({'error': 'Bot token not configured'}, status=400)
        
        # Get webhook URL from request or use default
        webhook_url = request.GET.get('url') or request.POST.get('url')
        if not webhook_url:
            # Try to construct from request
            scheme = request.scheme
            host = request.get_host()
            webhook_url = f"{scheme}://{host}/api/telegram/webhook/"
        
        url = f"https://api.telegram.org/bot{bot_token}/setWebhook"
        response = requests.post(url, json={
            'url': webhook_url
        }, timeout=10)
        
        result = response.json()
        
        if result.get('ok'):
            return JsonResponse({
                'success': True,
                'message': 'Webhook set successfully',
                'webhook_url': webhook_url,
                'result': result
            })
        else:
            return JsonResponse({
                'success': False,
                'error': result.get('description', 'Unknown error'),
                'result': result
            }, status=400)
            
    except Exception as e:
        return JsonResponse({
            'success': False,
            'error': str(e)
        }, status=500)

