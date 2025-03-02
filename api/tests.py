from django.test import TestCase
from django.urls import reverse
from rest_framework import status

from api.models import User, Order, Product, OrderItem


# Create your tests here.
class UserOrderTestCase(TestCase):
    def setUp(self):
        user1 = User.objects.create_user(username='user1', email='user1@gmail.com', password='user1@123')
        user2 = User.objects.create_user(username='user2', email='user2@gmail.com', password='user2@123')
        product1 = Product.objects.create(name="product1", description="product1 description", price=100, stock=8)
        product2 = Product.objects.create(name="product2", description="product2 description", price=101, stock=4)
        order1 = Order.objects.create(user=user1, status=Order.StatusChoices.CONFIRMED)
        OrderItem.objects.bulk_create([OrderItem(order=order1, product=product1, quantity=1),
                                       OrderItem(order=order1, product=product2, quantity=2)])
        order2 = Order.objects.create(user=user1, status=Order.StatusChoices.CONFIRMED)
        OrderItem.objects.bulk_create([OrderItem(order=order2, product=product2, quantity=1)])
        order3 = Order.objects.create(user=user2, status=Order.StatusChoices.CONFIRMED)
        OrderItem.objects.bulk_create([OrderItem(order=order3, product=product2, quantity=1),
                                       OrderItem(order=order3, product=product1, quantity=1)])

    def test_user_order_retrieves_only_authenticated_user_orders(self):
        user = User.objects.get(username='user1')
        self.client.force_login(user)
        response = self.client.get(reverse('api:order-list'))
        self.assertEqual(response.status_code, status.HTTP_200_OK)
        orders = response.json()
        print(orders)
        expected_user_url = f"http://testserver{reverse('api:user-detail', kwargs={'user_id': user.id})}"
        assert all(order['user'] == expected_user_url for order in orders)

    def test_user_order_list_unauthenticated(self):
        response = self.client.get(reverse('api:order-list'))
        self.assertEqual(response.status_code, status.HTTP_403_FORBIDDEN)
