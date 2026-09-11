from django.contrib import admin
from django.urls import path, include
from django.conf import settings
from django.conf.urls.static import static
from django.contrib.sitemaps import Sitemap
from django.urls import reverse
from products.models import Product, Category
from django.contrib.sitemaps.views import sitemap
from products.views import robots_txt

class StaticSitemap(Sitemap):
    changefreq = "weekly"
    priority = 0.8
    def items(self):
        return ['products:home', 'products:product_list', 'products:contact', 'products:about']
    def location(self, item):
        return reverse(item)

class ProductSitemap(Sitemap):
    changefreq = "daily"
    priority = 0.9
    def items(self):
        return Product.objects.filter(is_active=True)
    def lastmod(self, obj):
        return obj.updated_at

class CategorySitemap(Sitemap):
    changefreq = "weekly"
    priority = 0.7
    def items(self):
        return Category.objects.filter(is_active=True)

sitemaps = {
    'static': StaticSitemap,
    'products': ProductSitemap,
    'categories': CategorySitemap,
}

urlpatterns = [
    path('sitemap.xml', sitemap, {'sitemaps': sitemaps}, name='django.contrib.sitemaps.views.sitemap'),
    path('robots.txt', robots_txt, name='robots_txt'),
    path('', include('products.urls')),
    path('accounts/', include('accounts.urls')),
    path('cart/', include('cart.urls')),
    path('orders/', include('orders.urls')),
    path('reviews/', include('reviews.urls')),
    path("bankgateways/", include("azbankgateways.urls")),
    path("orders/", include("orders.urls")),
]

if settings.DEBUG:
    urlpatterns += static(settings.MEDIA_URL, document_root=settings.MEDIA_ROOT)