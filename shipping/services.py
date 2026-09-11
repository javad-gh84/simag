import random

def send_to_tipax(order, address):
    """ارسال اطلاعات به تیپاکس و دریافت کد رهگیری (شبیه‌سازی)"""
    # در واقعیت، اینجا باید به API تیپاکس متصل بشی
    tracking_code = f"TIPAX-{random.randint(100000, 999999)}"
    return tracking_code

def send_to_post(order, address):
    """ارسال اطلاعات به پست و دریافت کد رهگیری (شبیه‌سازی)"""
    tracking_code = f"POST-{random.randint(100000, 999999)}"
    return tracking_code