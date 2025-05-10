from django.urls import path
from . import views

urlpatterns = [
    path('', views.home, name='home'),
    path('products/', views.product_list, name='product_list'),
    path('product/<int:product_id>/', views.product_detail, name='product_detail'),
    path('dashboard/', views.admin_dashboard, name='admin_dashboard'),
    path('inventory/', views.inventory_management, name='inventory_management'),
    path('orders/', views.order_management, name='order_management'),
    path('orders/<int:order_id>/update/', views.update_order_status, name='update_order_status'),
]