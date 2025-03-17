from django.urls import path
from rest_framework.routers import DefaultRouter

from . import views

app_name = 'api'
router = DefaultRouter()
urlpatterns = [
    path('users', views.UserListAPIView.as_view(), name='users'),
    path('users/<int:user_id>', views.UserRetrieveAPIView.as_view(), name='user-detail'),
    path('products/', views.ProductListCreateApiView.as_view(), name='product-list', ),
    path('products/<int:product_id>', views.ProductRetrieveAPIView.as_view(), name='product-detail', ),
    path('products/info', views.ProductInfoListAPIView.as_view(), name='product-info', ),
]

router.register(r'orders', views.OrderViewSet)
urlpatterns += router.urls
