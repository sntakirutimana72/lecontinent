from datetime import datetime
from django.test import TestCase
from .serializers import ProductSerializer, OrderSerializer
from .models import Product


class ProductModelTestCases(TestCase):
    def setUp(self):
        self.placeholder = {
            'name': 'Juice',
            'description': 'Orange',
            'price': 33.5,
            'stock': 44,
        }

    def test_should_valid(self):
        serializer = ProductSerializer(data=self.placeholder)
        self.assertTrue(serializer.is_valid())

    def test_should_have_name(self):
        placeholder = {**self.placeholder}
        placeholder.pop('name')
        serializer = ProductSerializer(data=placeholder)
        self.assertFalse(serializer.is_valid())


class OrderModelTestCases(TestCase):
    def setUp(self):
        self.prodct_1 = Product.objects.create(name='juice', description='orange', price=22, stock=11)
        self.placeholder = {
            'customer_name': 'user',
            'customer_phone': '8797434',
            'order_date': datetime.now(),
            'status': 'pending',
            'total_price': 44,
            'products': [self.prodct_1.id],
        }

    def tearDown(self):
        Product.objects.all().delete()

    def test_should_valid(self):
        serializer = OrderSerializer(data=self.placeholder)
        serializer.is_valid()
        self.assertTrue(serializer.is_valid())

    def test_should_have_customer_name(self):
        placeholder = {**self.placeholder}
        placeholder.pop('customer_name')
        serializer = ProductSerializer(data=placeholder)
        self.assertFalse(serializer.is_valid())

    def test_should_have_status_and_should_be_pending_or_completed_or_canceled(self):
        placeholder = {**self.placeholder, 'status': 'ongoing'}
        serializer = OrderSerializer(data=placeholder)
        self.assertFalse(serializer.is_valid())
