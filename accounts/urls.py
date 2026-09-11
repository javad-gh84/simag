from django.urls import path
from . import views

app_name = 'accounts'

urlpatterns = [
    # ===== احراز هویت کاربر =====
    path('login/', views.login_view, name='login'),
    path('register/', views.register_view, name='register'),
    path('verify/', views.verify_view, name='verify'),
    path('resend/', views.resend_view, name='resend'),
    path('logout/', views.logout_view, name='logout'),
    
    # ===== احراز هویت ادمین =====
    path('admin-login/', views.admin_login_view, name='admin_login'),
    path('admin-logout/', views.admin_logout_view, name='admin_logout'),
    
    # ===== پنل کاربری =====
    path('profile/', views.user_dashboard, name='profile'),
    path('dashboard/', views.user_dashboard, name='dashboard'),
    path('orders/', views.user_orders, name='orders'),
    path('order/<int:order_id>/', views.order_detail, name='order_detail'),
    path('wishlist/', views.user_wishlist, name='wishlist'),
    path('wishlist/add/<int:product_id>/', views.add_to_wishlist, name='add_to_wishlist'),
    path('wishlist/remove/<int:product_id>/', views.remove_from_wishlist, name='remove_from_wishlist'),
    path('edit-profile/', views.edit_profile, name='edit_profile'),
    path('change-password/', views.change_password, name='change_password'),
    
    # ===== پنل مدیریت =====
    path('admin-dashboard/', views.admin_dashboard, name='admin_dashboard'),
    path('admin-orders/', views.admin_orders, name='admin_orders'),
    path('admin-order/<int:order_id>/', views.admin_order_detail, name='admin_order_detail'),
    path('admin-order/<int:order_id>/delete/', views.admin_order_delete, name='admin_order_delete'),
    path('admin-users/', views.admin_users, name='admin_users'),
    path('admin-user/<int:user_id>/', views.admin_user_detail, name='admin_user_detail'),
    path('admin-user/<int:user_id>/delete/', views.admin_user_delete, name='admin_user_delete'),
    path('admin-products/', views.admin_products, name='admin_products'),
    path('admin-product-add/', views.admin_product_add, name='admin_product_add'),
    path('admin-product-edit/<int:product_id>/', views.admin_product_edit, name='admin_product_edit'),
    path('admin-product-delete/<int:product_id>/', views.admin_product_delete, name='admin_product_delete'),
    path('admin-product-image-delete/<int:image_id>/', views.admin_product_image_delete, name='admin_product_image_delete'),
    path('admin-categories/', views.admin_categories, name='admin_categories'),
    path('admin-category-add/', views.admin_category_add, name='admin_category_add'),
    path('admin-category-edit/<int:category_id>/', views.admin_category_edit, name='admin_category_edit'),
    path('admin-category-delete/<int:category_id>/', views.admin_category_delete, name='admin_category_delete'),
]