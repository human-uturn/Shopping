from django.contrib import admin
from .models import Product, Order


@admin.register(Product)
class ProductAdmin(admin.ModelAdmin):
    list_display = ['product_number', 'name', 'category', 'quantity', 'price', 'created_at']
    list_filter = ['category', 'created_at']
    search_fields = ['product_number', 'name', 'category', 'description']
    readonly_fields = ['product_number', 'created_at', 'updated_at']
    fieldsets = (
        ('Product Information', {
            'fields': ('product_number', 'name', 'description', 'category')
        }),
        ('Pricing & Inventory', {
            'fields': ('price', 'quantity')
        }),
        ('Product Image', {
            'fields': ('picture',)
        }),
        ('Timestamps', {
            'fields': ('created_at', 'updated_at'),
            'classes': ('collapse',)
        }),
    )


@admin.register(Order)
class OrderAdmin(admin.ModelAdmin):
    list_display = ['order_number', 'created_at', 'total_amount']
    list_filter = ['created_at']
    search_fields = ['order_number']
    readonly_fields = ['order_number', 'created_at', 'items', 'total_amount']
    fieldsets = (
        ('Order Information', {
            'fields': ('order_number', 'created_at', 'total_amount', 'items')
        }),
    )
