from django.db import transaction
from rest_framework import serializers

from api.models import Product, Order, OrderItem, User


class UserSerializer(serializers.ModelSerializer):
    class Meta:
        model = User
        fields = ('id', 'username', 'email')


class ProductSerializer(serializers.ModelSerializer):
    class Meta:
        model = Product
        fields = ('id', 'name', 'price', 'stock', 'description')

    def validate_price(self, value):  # noqa
        if value <= 0:
            raise serializers.ValidationError('Price must be greater than 0')
        return value


class ProductInfoSerializer(serializers.Serializer):
    products = ProductSerializer(many=True)
    count = serializers.IntegerField()
    max_price = serializers.FloatField()


class OrderItemSerializer(serializers.ModelSerializer):
    name = serializers.CharField(source='product.name')
    price = serializers.DecimalField(source='product.price', max_digits=10, decimal_places=2)

    class Meta:
        model = OrderItem
        fields = ('name', 'price', 'quantity', 'item_subtotal')


class OrderSerializer(serializers.ModelSerializer):
    order_id = serializers.UUIDField(read_only=True)
    items = OrderItemSerializer(many=True, read_only=True)
    total_price = serializers.SerializerMethodField()
    user = serializers.HyperlinkedRelatedField(view_name='api:user-detail', read_only=True, lookup_field='id', lookup_url_kwarg='user_id')

    def get_total_price(self, obj: Order):
        return sum(order_item.item_subtotal for order_item in obj.items.all())

    class Meta:
        model = Order
        fields = ('order_id', 'status', 'user', 'created_at', 'items', 'total_price')


class OrderCreateSerializer(serializers.ModelSerializer):
    class OrderItemCreateSerializer(serializers.ModelSerializer):
        class Meta:
            model = OrderItem
            fields = ('product', 'quantity')

    items = OrderItemCreateSerializer(many=True, required=False)

    class Meta:
        model = Order
        fields = ('status', 'user', 'items')
        # setting user read_only to True because setting user value using serializer save from OrderModelViewSet
        extra_kwargs = {'user': {'read_only': True}}

    def create(self, validated_data):
        order_items = validated_data.pop('items', None)
        with transaction.atomic():
            order = Order.objects.create(**validated_data)
            if order_items:
                for order_item in order_items:
                    OrderItem.objects.create(order=order, **order_item)
        return order



    def update(self, instance: Order, validated_data):
        order_items = validated_data.pop('items', None)
        with transaction.atomic():
            order = super().update(instance, validated_data)
            if order_items:
                order.items.all().delete()
                for order_item in order_items:
                    OrderItem.objects.create(order=order, **order_item)
            else:
                order.items.all().delete()
            order.refresh_from_db()
        return order
