import random
from datetime import datetime
from rest_framework import status
from rest_framework.reverse import reverse
from rest_framework.test import APITestCase, APIClient
from .serializers import ProductSerializer, OrderSerializer
from .models import Product, Order
from .serializers import ProductSerializer


class ProductModelTestCases(APITestCase):
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


class OrderModelTestCases(APITestCase):
    def setUp(self):
        product = Product.objects.create(name='juice', description='orange', price=22, stock=11)
        self.placeholder = {
            'customer_name': 'user',
            'customer_phone': '8797434',
            'order_date': datetime.now(),
            'status': 'pending',
            'total_price': 44,
            'products': [product.id],
        }

    def tearDown(self):
        Product.objects.all().delete()

    def test_should_be_valid(self):
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


# noinspection PyUnresolvedReferences
class ProductIndexViewTestCases(APITestCase):
    def setUp(self):
        self.client = APIClient()

    def tearDown(self):
        Order.objects.all().delete()
        Product.objects.all().delete()

    @property
    def prod_dummy(self):
        # Create a dummy product model instance
        return {
            'name': f'new_dummy_prod_name',
            'description': f'new_dummy_prod_desc',
            'stock': 48.5,
            'price': 11.04,
        }

    @staticmethod
    def route_url(*args, **kwargs):
        return reverse('prod-index', args=args, kwargs=kwargs)

    def test_create_successfully(self):
        self.assertFalse(Product.objects.exists())
        response = self.client.post(self.route_url(), data=self.prod_dummy)
        self.assertEquals(response.status_code, status.HTTP_201_CREATED)
        self.assertTrue(Product.objects.exists())
        # Data from db
        from_db = Product.objects.first()
        from_db_serial = ProductSerializer(from_db).data
        from_res = response.json()
        self.assertEqual(from_db_serial, from_res)

    def test_create_without_name(self):
        invalid_dummy = self.prod_dummy
        # Remove name key
        invalid_dummy.pop('name')
        self.assertFalse(Product.objects.exists())
        response = self.client.post(self.route_url(), data=invalid_dummy)
        self.assertEquals(response.status_code, status.HTTP_422_UNPROCESSABLE_ENTITY)
        self.assertFalse(Product.objects.exists())

    def test_update_successfully(self):
        sample = Product.objects.create(**self.prod_dummy)
        og_last_update_date = sample.updated_at
        og_stock = sample.stock
        url = reverse('prod-details', args=(sample.pk,))
        response = self.client.put(url, data={'stock': sample.stock + 7})
        self.assertEquals(response.status_code, status.HTTP_200_OK)
        sample.refresh_from_db()
        self.assertNotEquals(og_last_update_date, sample.updated_at)
        self.assertNotEquals(og_stock, sample.stock)
