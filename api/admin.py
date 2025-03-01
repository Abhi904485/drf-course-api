from django.contrib import admin

# Register your models here.
from .models import OrderItem, Product, Order, User
admin.site.register(OrderItem)
admin.site.register(Product)
admin.site.register(User)
admin.site.register(Order)