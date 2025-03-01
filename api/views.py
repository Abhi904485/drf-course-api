from django.db.models import Max
from rest_framework.generics import ListAPIView, RetrieveAPIView
from rest_framework.response import Response

from api.models import Product, Order, User
from api.serializers import (ProductSerializer, OrderSerializer, UserSerializer, ProductInfoSerializer)


class UserListAPIView(ListAPIView):
    queryset = User.objects.all()
    serializer_class = UserSerializer


class UserRetrieveAPIView(RetrieveAPIView):
    queryset = User.objects.all()
    serializer_class = UserSerializer
    lookup_url_kwarg = 'user_id'


class ProductListApiView(ListAPIView):
    queryset = Product.objects.all()
    serializer_class = ProductSerializer


class ProductRetrieveAPIView(RetrieveAPIView):
    queryset = Product.objects.all()
    serializer_class = ProductSerializer
    lookup_url_kwarg = 'product_id'


class OrderListAPIView(ListAPIView):
    queryset = Order.objects.all()
    serializer_class = OrderSerializer


class OrderRetrieveAPIView(RetrieveAPIView):
    queryset = Order.objects.all()
    serializer_class = OrderSerializer
    lookup_url_kwarg = 'order_id'


class ProductInfoListAPIView(ListAPIView):
    queryset = Product.objects.all()
    serializer_class = ProductInfoSerializer

    def get(self, request, *args, **kwargs):
        data = {"products": self.get_queryset(), "count": self.get_queryset().count(),
                "max_price": self.get_queryset().aggregate(max_price=Max("price"))["max_price"]}
        serializer = self.get_serializer(data)
        return Response(serializer.data)
