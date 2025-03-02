from django.contrib import admin

# Register your models here.
from .models import OrderItem, Product, Order, User

admin.site.register(Product)
admin.site.register(User)


class OrderItemInline(admin.TabularInline):
    model = OrderItem
    extra = 1


class OrderAdmin(admin.ModelAdmin):
    inlines = (OrderItemInline,)


admin.site.register(Order, OrderAdmin)
