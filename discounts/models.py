from django.db import models
from django.utils.timezone import now

class DiscountCode(models.Model):
    DISCOUNT_TYPE = (
        ('percentage', 'درصدی'),
        ('fixed', 'مبلغ ثابت'),
    )

    code = models.CharField(max_length=50, unique=True)
    discount_type = models.CharField(max_length=10, choices=DISCOUNT_TYPE)
    value = models.PositiveIntegerField()  # درصد یا مبلغ ثابت
    max_usage = models.PositiveIntegerField(default=1)
    used_count = models.PositiveIntegerField(default=0)
    valid_from = models.DateTimeField()
    valid_to = models.DateTimeField()
    is_active = models.BooleanField(default=True)

    def is_valid(self):
        return (self.is_active and
                self.used_count < self.max_usage and
                self.valid_from <= now() <= self.valid_to)

    def __str__(self):
        return self.code