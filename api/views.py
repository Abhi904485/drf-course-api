from django.db.models import Max
from django.shortcuts import get_object_or_404
from rest_framework.decorators import api_view
from rest_framework.response import Response

from api.models import Product, Order, User
from api.serializers import ProductSerializer, OrderSerializer, UserSerializer, ProductInfoSerializer


@api_view(['GET'])
def user_list(request):
    users = User.objects.all()
    serializer = UserSerializer(users, many=True, context={'request': request})
    return Response(serializer.data)


@api_view(['GET'])
def user_detail(request, pk):
    user = get_object_or_404(User, pk=pk)
    serializer = UserSerializer(user, context={'request': request})
    return Response(serializer.data)


@api_view(http_method_names=['GET'])
def product_list(request):
    products = Product.objects.all()
    serializer = ProductSerializer(products, many=True)
    return Response(serializer.data)


@api_view(http_method_names=['GET'])
def product_detail(request, pk):
    product = get_object_or_404(Product, pk=pk)
    serializer = ProductSerializer(product)
    return Response(serializer.data)


@api_view(http_method_names=['GET'])
def order_list(request):
    orders = Order.objects.all()
    serializer = OrderSerializer(orders, many=True, context={'request': request})
    return Response(serializer.data)


@api_view(http_method_names=['GET'])
def order_detail(request, order_id):
    order = get_object_or_404(Order, order_id=order_id)
    serializer = OrderSerializer(order, context={'request': request})
    return Response(serializer.data)


@api_view(http_method_names=['GET'])
def product_info(request):
    products = Product.objects.all()
    serializer = ProductInfoSerializer({"products": products, "count": len(products),
                                        "max_price": products.aggregate(max_price=Max("price"))["max_price"]})
    return Response(serializer.data)
