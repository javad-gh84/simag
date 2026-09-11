import requests
from django.conf import settings

def send_sms(phone, message):
    """
    ارسال پیامک با کاوه نگار
    """
    # ===== حالت تست (Mock) =====
    if getattr(settings, 'SMS_MOCK', True):
        print(f"📱 [MOCK SMS] به {phone}: {message}")
        return {'success': True, 'message': 'Mock mode'}
    
    # ===== ارسال واقعی با کاوه نگار =====
    api_key = settings.KAVENEGAR_API_KEY
    sender = settings.KAVENEGAR_SENDER
    
    url = f'https://api.kavenegar.com/v1/{api_key}/sms/send.json'
    data = {
        'sender': sender,
        'receptor': phone,
        'message': message
    }
    
    try:
        response = requests.post(url, data=data, timeout=10)
        result = response.json()
        
        if result.get('return', {}).get('status') == 200:
            return {'success': True, 'message': 'ارسال شد'}
        else:
            return {'success': False, 'message': 'خطا در ارسال'}
    except:
        return {'success': False, 'message': 'خطا در ارتباط با سرور'}


def send_otp_code(phone, code):
    """ارسال کد تایید"""
    message = f"✅ کد تایید شما: {code}\n\nسیماگ"
    return send_sms(phone, message)


def send_order_status_notification(user, order, status):
    """ارسال تغییر وضعیت سفارش"""
    status_names = {
        'pending': 'در انتظار',
        'processing': 'در حال پردازش',
        'shipped': 'ارسال شده',
        'delivered': 'تحویل داده شده',
        'cancelled': 'لغو شده',
    }
    
    message = (
        f"🛒 وضعیت سفارش #{order.order_number} شما تغییر کرد.\n"
        f"وضعیت جدید: {status_names.get(status, status)}\n\n"
        f"سیماگ"
    )
    return send_sms(user.phone, message)