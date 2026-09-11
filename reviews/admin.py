from django.contrib import admin
from django.utils.html import format_html
from .models import Review


@admin.register(Review)
class ReviewAdmin(admin.ModelAdmin):
    list_display = ['product', 'user', 'rating_display', 'comment_preview', 'is_approved', 'created_at']
    list_filter = ['is_approved', 'rating', 'created_at']
    search_fields = ['product__name', 'user__phone', 'comment']
    readonly_fields = ['created_at', 'updated_at']
    list_editable = ['is_approved']
    actions = ['approve_reviews', 'unapprove_reviews']
    
    def rating_display(self, obj):
        return '★' * obj.rating + '☆' * (5 - obj.rating)
    rating_display.short_description = 'امتیاز'
    
    def comment_preview(self, obj):
        return obj.comment[:50] + '...' if len(obj.comment) > 50 else obj.comment
    comment_preview.short_description = 'نظر'
    
    def approve_reviews(self, request, queryset):
        queryset.update(is_approved=True)
        self.message_user(request, f'{queryset.count()} نظر تایید شد.')
    approve_reviews.short_description = 'تایید نظرات انتخاب‌شده'
    
    def unapprove_reviews(self, request, queryset):
        queryset.update(is_approved=False)
        self.message_user(request, f'{queryset.count()} نظر لغو تایید شد.')
    unapprove_reviews.short_description = 'لغو تایید نظرات انتخاب‌شده'