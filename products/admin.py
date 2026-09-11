from django.contrib import admin
from django.utils.html import format_html
from .models import Category, Product, ProductVariant, ProductImage, Wishlist

class ProductImageInline(admin.TabularInline):
    model = ProductImage
    extra = 1
    fields = ['image', 'is_main', 'order']
    readonly_fields = ['id']

class ProductVariantInline(admin.TabularInline):
    model = ProductVariant
    extra = 1
    fields = ['barcode', 'color', 'size', 'stock', 'price_adjustment']
    readonly_fields = ['id']

@admin.register(Category)
class CategoryAdmin(admin.ModelAdmin):
    list_display = ['name', 'slug', 'image_preview', 'product_count', 'is_active']
    list_filter = ['is_active']
    search_fields = ['name', 'slug']
    prepopulated_fields = {'slug': ('name',)}
    ordering = ['name']
    
    def image_preview(self, obj):
        if obj.image:
            return format_html(f'<img src="{obj.image.url}" style="width:50px;height:50px;object-fit:cover;border-radius:8px;">')
        return '-'
    image_preview.short_description = 'تصویر'
    
    def product_count(self, obj):
        return obj.products.filter(is_active=True).count()
    product_count.short_description = 'تعداد محصولات'

@admin.register(Product)
class ProductAdmin(admin.ModelAdmin):
    list_display = ['name', 'category', 'price', 'is_featured', 'is_active', 'created_at']
    list_filter = ['category', 'is_active', 'is_featured', 'created_at']
    search_fields = ['name', 'brand', 'slug']
    prepopulated_fields = {'slug': ('name',)}
    ordering = ['-created_at']
    inlines = [ProductImageInline, ProductVariantInline]

@admin.register(ProductVariant)
class ProductVariantAdmin(admin.ModelAdmin):
    list_display = ['product', 'color', 'size', 'stock', 'price_adjustment']
    list_filter = ['color']
    search_fields = ['barcode', 'product__name']
    ordering = ['product', 'color']

@admin.register(ProductImage)
class ProductImageAdmin(admin.ModelAdmin):
    list_display = ['product', 'image_preview', 'is_main', 'order']
    list_filter = ['is_main']
    search_fields = ['product__name']
    ordering = ['product', 'order']
    
    def image_preview(self, obj):
        if obj.image:
            return format_html(f'<img src="{obj.image.url}" style="width:50px;height:50px;object-fit:cover;border-radius:8px;">')
        return '-'
    image_preview.short_description = 'پیش‌نمایش'

@admin.register(Wishlist)
class WishlistAdmin(admin.ModelAdmin):
    list_display = ['user', 'product_count', 'created_at']
    search_fields = ['user__phone', 'user__full_name']
    filter_horizontal = ['products']
    
    def product_count(self, obj):
        return obj.products.count()
    product_count.short_description = 'تعداد محصولات'