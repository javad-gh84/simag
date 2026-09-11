from pathlib import Path
import os

BASE_DIR = Path(__file__).resolve().parent.parent

SECRET_KEY = 'django-insecure-fcej!z!!ln)h@ei=fnfxv(g3%$!z&w!e)+38&y$rdxpm(lq6c4'

DEBUG = True
ALLOWED_HOSTS = ['127.0.0.1', 'localhost']

INSTALLED_APPS = [
    'django.contrib.admin',
    'django.contrib.auth',
    'django.contrib.contenttypes',
    'django.contrib.sessions',
    'django.contrib.messages',
    'django.contrib.staticfiles',
    'django.contrib.sitemaps',
    'products',
    'cart',
    'orders',
    'discounts',
    'reviews',
    'shipping',
    'barcode',
    'accounts',
    # "azbankgateways",
]

AUTH_USER_MODEL = 'accounts.User'

MIDDLEWARE = [
    'django.middleware.security.SecurityMiddleware',
    'django.contrib.sessions.middleware.SessionMiddleware',
    'django.middleware.common.CommonMiddleware',
    'django.middleware.csrf.CsrfViewMiddleware',
    'django.contrib.auth.middleware.AuthenticationMiddleware',
    'django.contrib.messages.middleware.MessageMiddleware',
    'django.middleware.clickjacking.XFrameOptionsMiddleware',
]

ROOT_URLCONF = 'simag.urls'

TEMPLATES = [
    {
        'BACKEND': 'django.template.backends.django.DjangoTemplates',
        'DIRS': [BASE_DIR / 'templates'],
        'APP_DIRS': True,
        'OPTIONS': {
            'context_processors': [
                'django.template.context_processors.request',
                'django.contrib.auth.context_processors.auth',
                'django.contrib.messages.context_processors.messages',
            ],
        },
    },
]

WSGI_APPLICATION = 'simag.wsgi.application'

DATABASES = {
    'default': {
        'ENGINE': 'django.db.backends.sqlite3',
        'NAME': BASE_DIR / 'db.sqlite3',
    }
}

AUTH_PASSWORD_VALIDATORS = [
    {'NAME': 'django.contrib.auth.password_validation.UserAttributeSimilarityValidator'},
    {'NAME': 'django.contrib.auth.password_validation.MinimumLengthValidator'},
    {'NAME': 'django.contrib.auth.password_validation.CommonPasswordValidator'},
    {'NAME': 'django.contrib.auth.password_validation.NumericPasswordValidator'},
]

LANGUAGE_CODE = 'fa-ir'
TIME_ZONE = 'Asia/Tehran'
USE_I18N = True
USE_TZ = True

STATIC_URL = '/static/'
STATICFILES_DIRS = [os.path.join(BASE_DIR, 'static')]
STATIC_ROOT = os.path.join(BASE_DIR, 'staticfiles')

MEDIA_URL = '/media/'
MEDIA_ROOT = os.path.join(BASE_DIR, 'media')

EMAIL_BACKEND = 'django.core.mail.backends.console.EmailBackend'

# ===== Login URLs =====
LOGIN_URL = 'accounts:login'
LOGIN_REDIRECT_URL = 'products:home'
LOGOUT_REDIRECT_URL = 'products:home'

# ===== SMS Settings =====
SMS_PROVIDER = 'kavenegar'  # انتخاب: kavenegar, farazsms, smsir

# کاوه نگار
KAVENEGAR_API_KEY = 'API-Key-ای-که-گرفتی'  # <== اینجا بذار
KAVENEGAR_SENDER = '1000596446'  # شماره خط ارسال

# حالت تست (برای تست بدون ارسال واقعی)
SMS_MOCK = False  # True = فقط توی ترمینال نشون بده، False = ارسال واقعی

AUTHENTICATION_BACKENDS = [
    'accounts.backends.PhoneBackend',
    'django.contrib.auth.backends.ModelBackend',  # برای حفظ حالت پیش‌فرض
]



# AZ_IRANIAN_BANK_GATEWAYS = {
#     "GATEWAYS": {
#         "ZARINPAL": {
#             "MERCHANT_CODE": "YOUR-MERCHANT-CODE-HERE",  # کد مرچنت زرین‌پال
#             "DESCRIPTION": "پرداخت سفارش از فروشگاه سیماگ",
#             "CALLBACK_URL": "http://127.0.0.1:8000/orders/payment/callback/",  # توی پروداکشن دامنه‌ت رو بذار
#             "IS_SAMPLE_FORM_ENABLE": False,  # چون خودمون فرم داریم
#         },
#     },
#     "IS_SAFE_GET_GATEWAY_PAYMENT": True,  # جلوگیری از تغییر مبلغ توسط کاربر
#     "CURRENCY": "IRR",  # واحد پول: IRR (ریال) یا IRT (تومان)
#     "TRACKING_CODE_QUERY_PARAM": "tc",  # پارامتر کد پیگیری توی URL
#     "TRACKING_CODE_LENGTH": 12,
#     "SETTING_VALUE_READER_CLASS": "azbankgateways.readers.DefaultReader",
#     "BANK_PRIORITIES": ["ZARINPAL"],
#     "IS_HEADER_ACCEPT_ENCODING_ENABLE": True,
# }