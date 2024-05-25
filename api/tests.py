import random
from datetime import datetime
from rest_framework import status
from rest_framework.response import Response
from rest_framework.reverse import reverse
from rest_framework.test import APITestCase, APIClient
from .serializers import ProductSerializer, OrderSerializer
from .models import Product, Order


# noinspection PyUnresolvedReferences
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


# noinspection PyUnresolvedReferences
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
class ProductViewsTestCase(APITestCase):
    urlName: str
    response: Response

    def setUp(self):
        self.client = APIClient()
        self.prod_dummy = {
            'name': f'new_dummy_prod_name',
            'description': f'new_dummy_prod_desc',
            'stock': 48.5,
            'price': 11.04,
        }

    def tearDown(self):
        Order.objects.all().delete()
        Product.objects.all().delete()

    def create_prod(self):
        record = Product.objects.create(**self.prod_dummy)
        return record

    def get_url(self, *args, **kwargs):
        return reverse(self.urlName, args=args, kwargs=kwargs)

    def assertStatus(self, status_code: int):
        self.assertEquals(self.response.status_code, status_code)


# noinspection PyUnresolvedReferences
class ProductIndexViewTests(ProductViewsTestCase):
    def setUp(self):
        self.urlName = 'prod-index'
        super().setUp()

    def test_get_all_products(self):
        count = 3
        instance_list = [Product(**attrs) for attrs in ([self.prod_dummy] * count)]
        Product.objects.bulk_create(instance_list)
        self.response = self.client.get(self.get_url())
        self.assertStatus(status.HTTP_200_OK)
        products_list = self.response.json()
        self.assertEquals(len(products_list), count)
        expected = ProductSerializer(Product.objects.all(), many=True).data
        self.assertEqual(products_list, expected)

    def test_create_product_successfully(self):
        self.assertFalse(Product.objects.exists())
        self.response = self.client.post(self.get_url(), data=self.prod_dummy)
        self.assertStatus(status.HTTP_201_CREATED)
        self.assertTrue(Product.objects.exists())
        # Data from db
        from_db = Product.objects.first()
        from_db_serial = ProductSerializer(from_db).data
        from_res = self.response.json()
        self.assertEqual(from_db_serial, from_res)

    def test_create_product_without_name(self):
        invalid_dummy = self.prod_dummy
        # Remove name key
        invalid_dummy.pop('name')
        self.assertFalse(Product.objects.exists())
        self.response = self.client.post(self.get_url(), data=invalid_dummy)
        self.assertStatus(status.HTTP_422_UNPROCESSABLE_ENTITY)
        self.assertFalse(Product.objects.exists())


# noinspection PyUnresolvedReferences
class ProductDetailsViewTests(ProductViewsTestCase):
    def setUp(self):
        self.urlName = 'prod-details'
        super().setUp()

    def test_get_specific_product_by_id(self):
        sample = self.create_prod()
        self.response = self.client.get(self.get_url(sample.pk))
        self.assertStatus(status.HTTP_200_OK)
        from_be = self.response.json()
        self.assertIn('id', from_be)
        self.assertEquals(sample.pk, from_be['id'])

    def test_get_non_existing_product_by_id(self):
        self.response = self.client.get(self.get_url(879898))
        self.assertStatus(status.HTTP_404_NOT_FOUND)

    def test_update_successfully(self):
        sample = self.create_prod()
        og_last_update_date = sample.updated_at
        og_stock = sample.stock
        response = self.client.put(self.get_url(sample.pk), data={'stock': sample.stock + 7})
        self.assertEquals(response.status_code, status.HTTP_200_OK)
        sample.refresh_from_db()
        self.assertNotEquals(og_last_update_date, sample.updated_at)
        self.assertNotEquals(og_stock, sample.stock)

    def test_update_on_non_existing(self):
        response = self.client.put(self.get_url(9878), data={'name': 'flour'})
        self.assertEquals(response.status_code, status.HTTP_404_NOT_FOUND)
