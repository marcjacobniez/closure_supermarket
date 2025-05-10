from django.contrib import admin
from .models import Category, Product

@admin.register(Category)
class CategoryAdmin(admin.ModelAdmin):
    list_display = ['name']
    search_fields = ['name']

@admin.register(Product)
class ProductAdmin(admin.ModelAdmin):
    list_display = ['name', 'price', 'category', 'stock_quantity', 'available']
    list_filter = ['available', 'category']
    list_editable = ['price', 'stock_quantity', 'available']
    search_fields = ['name', 'description']
