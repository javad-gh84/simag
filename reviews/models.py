from django.db import models
from django.conf import settings
from products.models import Product


class Review(models.Model):
    """مدل نظرات و امتیازات محصولات"""
    
    product = models.ForeignKey(
        Product, 
        on_delete=models.CASCADE, 
        related_name='reviews',
        verbose_name='محصول'
    )
    user = models.ForeignKey(
        settings.AUTH_USER_MODEL, 
        on_delete=models.CASCADE, 
        related_name='reviews',
        verbose_name='کاربر'
    )
    rating = models.PositiveSmallIntegerField(
        choices=[(i, i) for i in range(1, 6)], 
        default=5,
        verbose_name='امتیاز'
    )
    comment = models.TextField(
        verbose_name='نظر'
    )
    is_approved = models.BooleanField(
        default=False,
        verbose_name='تایید شده'
    )
    created_at = models.DateTimeField(
        auto_now_add=True,
        verbose_name='تاریخ ایجاد'
    )
    updated_at = models.DateTimeField(
        auto_now=True,
        verbose_name='تاریخ ویرایش'
    )

    class Meta:
        ordering = ['-created_at']
        unique_together = ('product', 'user')
        verbose_name = 'نظر'
        verbose_name_plural = 'نظرات'

    def __str__(self):
        return f"{self.user.phone} - {self.product.name} - {self.rating}★"

    @property
    def rating_stars(self):
        """نمایش امتیاز به صورت ستاره"""
        return '★' * self.rating + '☆' * (5 - self.rating)

    @property
    def short_comment(self):
        """نمایش خلاصه نظر"""
        return self.comment[:50] + '...' if len(self.comment) > 50 else self.comment