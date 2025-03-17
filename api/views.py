from django.db.models import Max
from django_filters.rest_framework import DjangoFilterBackend
from rest_framework import viewsets
from rest_framework.filters import SearchFilter, OrderingFilter
from rest_framework.generics import ListAPIView, RetrieveAPIView, ListCreateAPIView, RetrieveUpdateDestroyAPIView
from rest_framework.permissions import IsAuthenticated, IsAdminUser, AllowAny
from rest_framework.response import Response

from api.filter import ProductFilterSet, InStockProductFilterBackend, OrderFilterSet
from api.models import Product, Order, User
from api.serializers import (ProductSerializer, OrderSerializer, UserSerializer, ProductInfoSerializer,
                             OrderCreateSerializer)


class UserListAPIView(ListAPIView):
    queryset = User.objects.all()
    serializer_class = UserSerializer


class UserRetrieveAPIView(RetrieveAPIView):
    queryset = User.objects.all()
    serializer_class = UserSerializer
    lookup_url_kwarg = 'user_id'


class ProductListCreateApiView(ListCreateAPIView):
    queryset = Product.objects.all()
    serializer_class = ProductSerializer
    filterset_class = ProductFilterSet
    filter_backends = [DjangoFilterBackend, SearchFilter, OrderingFilter, InStockProductFilterBackend]
    search_fields = ['name', 'price', 'stock']
    ordering_fields = ['name', 'price', 'stock']


    def get_permissions(self):
        self.permission_classes = [AllowAny]
        if self.request.method == 'POST':
            self.permission_classes = [IsAdminUser]
        return super().get_permissions()


class ProductRetrieveAPIView(RetrieveUpdateDestroyAPIView):
    queryset = Product.objects.all()
    serializer_class = ProductSerializer
    lookup_url_kwarg = 'product_id'

    def get_permissions(self):
        self.permission_classes = [AllowAny]
        if self.request.method in ['PUT', 'PATCH', 'DELETE']:
            self.permission_classes = [IsAdminUser]
        return super().get_permissions()


class OrderViewSet(viewsets.ModelViewSet):
    queryset = Order.objects.all()
    serializer_class = OrderSerializer
    lookup_url_kwarg = 'order_id'
    permission_classes = (IsAuthenticated,)
    pagination_class = None
    filterset_class = OrderFilterSet
    filter_backends = [DjangoFilterBackend, SearchFilter, OrderingFilter]
    ordering_fields = ['status', 'created_at']
    search_fields = ['status', 'created_at']

    def get_queryset(self):
        if not self.request.user.is_staff:
            return super().get_queryset().filter(user=self.request.user)
        return super().get_queryset()

    def get_serializer_class(self):
        if self.action in ["create", "update", "partial_update"]:
            return OrderCreateSerializer
        return super().get_serializer_class()

    def perform_create(self, serializer):
        # Saving extra info user not passing from request body
        serializer.save(user=self.request.user)

    def perform_update(self, serializer):
        serializer.save(user=self.request.user)




class ProductInfoListAPIView(ListAPIView):
    queryset = Product.objects.all()
    serializer_class = ProductInfoSerializer

    def get(self, request, *args, **kwargs):
        data = {"products": self.get_queryset(), "count": self.get_queryset().count(),
                "max_price": self.get_queryset().aggregate(max_price=Max("price"))["max_price"]}
        serializer = self.get_serializer(data)
        return Response(serializer.data)
