from django.db import models
from django.contrib.auth.models import AbstractUser, BaseUserManager

class UserManager(BaseUserManager):
    def create_user(self, phone, email=None, password=None, **extra_fields):
        if not phone:
            raise ValueError('شماره موبایل الزامی است')
        email = self.normalize_email(email) if email else None
        user = self.model(phone=phone, email=email, **extra_fields)
        user.set_password(password)
        user.save(using=self._db)
        return user

    def create_superuser(self, phone, email=None, password=None, **extra_fields):
        extra_fields.setdefault('is_staff', True)
        extra_fields.setdefault('is_superuser', True)
        extra_fields.setdefault('is_active', True)
        extra_fields.setdefault('is_verified', True)
        return self.create_user(phone, email, password, **extra_fields)


class User(AbstractUser):
    username = None
    phone = models.CharField(max_length=11, unique=True)
    is_verified = models.BooleanField(default=False)
    full_name = models.CharField(max_length=100, blank=True, null=True)
    email = models.EmailField(blank=True, null=True)
    address = models.TextField(blank=True, null=True)
    postal_code = models.CharField(max_length=10, blank=True, null=True)

    USERNAME_FIELD = 'phone'
    REQUIRED_FIELDS = ['email']
    objects = UserManager()

    def save(self, *args, **kwargs):
        if not self.username:
            self.username = f"user_{self.phone}"
        super().save(*args, **kwargs)

    def __str__(self):
        return self.phone


class OTPCode(models.Model):
    user = models.ForeignKey(User, on_delete=models.CASCADE)
    code = models.CharField(max_length=6)
    created_at = models.DateTimeField(auto_now_add=True)
    is_used = models.BooleanField(default=False)

    def is_valid(self):
        from django.utils.timezone import now
        return not self.is_used and (now() - self.created_at).seconds < 120

    def __str__(self):
        return f"{self.user.phone} - {self.code}"