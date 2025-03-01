import uuid

from django.contrib.auth.models import AbstractUser
from django.db import models

from api.manager import OrderManager


class User(AbstractUser):
    pass


class Product(models.Model):
    name = models.CharField(max_length=200)
    description = models.TextField()
    price = models.DecimalField(decimal_places=2, max_digits=10)
    stock = models.PositiveIntegerField()
    image = models.ImageField(upload_to='products/', null=True, blank=True)

    class Meta:
        db_table = 'product'
        verbose_name = 'Product'
        verbose_name_plural = 'Products'

    @property
    def in_stock(self):
        return self.stock > 0

    def __str__(self):
        return self.name


class Order(models.Model):
    class StatusChoices(models.TextChoices):
        PENDING = 'PENDING'
        PROCESSING = 'PROCESSING'
        COMPLETED = 'COMPLETED'
        CONFIRMED = 'CONFIRMED'
        CANCELED = 'CANCELED'

    order_id = models.UUIDField(primary_key=True, default=uuid.uuid4, editable=False)
    user = models.ForeignKey(User, on_delete=models.CASCADE, related_name='orders', related_query_name='order')
    created_at = models.DateTimeField(auto_now_add=True)
    status = models.CharField(max_length=10, choices=StatusChoices, default=StatusChoices.PENDING)
    product = models.ManyToManyField(Product, through="OrderItem", through_fields=("order", "product"),
                                     related_name="orders", related_query_name="order")

    objects = OrderManager()

    class Meta:
        db_table = 'order'
        verbose_name = 'Order'
        verbose_name_plural = 'Orders'

    def __str__(self):
        return f"{self.order_id} by {self.user.username}"


class OrderItem(models.Model):
    product = models.ForeignKey(Product, on_delete=models.CASCADE, related_name='items', related_query_name='item')
    order = models.ForeignKey(Order, on_delete=models.CASCADE, related_name='items', related_query_name='item')
    quantity = models.PositiveIntegerField()

    class Meta:
        db_table = 'order_item'
        verbose_name = 'Order Item'
        verbose_name_plural = 'Order Items'

    @property
    def item_subtotal(self):
        return self.quantity * self.product.price

    def __str__(self):
        return f"{self.quantity} * {self.product.name} in order {self.order.order_id} "
