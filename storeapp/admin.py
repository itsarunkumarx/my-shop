# from django.contrib import admin
# from .models import (Category,Product,Customer,Order,OrderItem,Review)


# admin.site.register(Category)
# admin.site.register(Product)
# admin.site.register(Customer)
# admin.site.register(Order)
# admin.site.register(OrderItem)
# admin.site.register(Review)

from django.contrib import admin
from .models import (
    Category,
    Product,
    Customer,
    Order,
    OrderItem,
    Review
)


# Category Admin
@admin.register(Category)
class CategoryAdmin(admin.ModelAdmin):
    list_display = (
        'id',
        'name',
        'description',
    )

    search_fields = (
        'name',
    )


# Product Admin
@admin.register(Product)
class ProductAdmin(admin.ModelAdmin):
    list_display = (
        'id',
        'name',
        'category',
        'price',
        'stock',
        'is_available',
    )

    list_filter = (
        'category',
        'is_available',
    )

    search_fields = (
        'name',
        'description',
    )


# Customer Admin
@admin.register(Customer)
class CustomerAdmin(admin.ModelAdmin):
    list_display = (
        'id',
        'user',
        'phone',
        'city',
        'state',
        'pincode',
    )

    search_fields = (
        'user__username',
        'phone',
        'city',
    )


# Order Admin
@admin.register(Order)
class OrderAdmin(admin.ModelAdmin):
    list_display = (
        'id',
        'customer',
        'total_amount',
        'status',
        'created_at',
    )

    list_filter = (
        'status',
        'created_at',
    )

    search_fields = (
        'customer__user__username',
    )


# Order Item Admin
@admin.register(OrderItem)
class OrderItemAdmin(admin.ModelAdmin):
    list_display = (
        'id',
        'order',
        'product',
        'quantity',
        'price',
    )

    search_fields = (
        'product__name',
    )


# Review Admin
@admin.register(Review)
class ReviewAdmin(admin.ModelAdmin):
    list_display = (
        'id',
        'product',
        'user',
        'rating',
        'created_at',
    )

    list_filter = (
        'rating',
        'created_at',
    )

    search_fields = (
        'product__name',
        'user__username',
    )
