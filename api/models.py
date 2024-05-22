from django.db import models
from .helpers import validate_order_status


ORDER_STATUS_CHOICES = [
    ('pending', 'pending'),
    ('completed', 'completed'),
    ('canceled', 'canceled')
]


class Product(models.Model):
    name = models.CharField(max_length=255)
    description = models.CharField(max_length=255)
    price = models.FloatField()
    stock = models.FloatField()
    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)


class Order(models.Model):
    customer_name = models.CharField(max_length=255)
    customer_phone = models.CharField(max_length=255)
    order_date = models.DateTimeField()
    status = models.CharField(
        default='pending',
        max_length=10,
        choices=ORDER_STATUS_CHOICES,
        validators=[validate_order_status(ORDER_STATUS_CHOICES)]
    )
    products = models.ManyToManyField(Product, related_name='products')
    total_price = models.FloatField()
