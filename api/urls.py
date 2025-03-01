from django.urls import path

from . import views

app_name = 'api'
urlpatterns = [
    path('users', views.user_list, name='users'),
    path('users/<int:pk>', views.user_detail, name='user-detail'),
    path('products/', views.product_list, name='product-list', ),
    path('products/<int:pk>', views.product_detail, name='product-detail', ),
    path('products/info', views.product_info, name='product-info', ),
    path('orders/', views.order_list, name='order-list', ),
    path('orders/<uuid:order_id>', views.order_detail, name='order-detail', ),
]
