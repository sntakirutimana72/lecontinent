import json

from rest_framework import serializers
from django.core.serializers import serialize
from .models import Product, Order


def serialize_order(queryset, single=False):
    payload = serialize('json', queryset, fields=[
        'id', 'customer_name', 'customer_phone', 'order_date', 'status', 'total_price', 'products'
    ])
    data = json.loads(payload)
    return data[0] if single else data


class ProductSerializer(serializers.ModelSerializer):
    class Meta:
        model = Product
        fields = ['id', 'name', 'description', 'price', 'stock', 'created_at', 'updated_at']


class OrderSerializer(serializers.ModelSerializer):
    class Meta:
        model = Order
        fields = ['id', 'customer_name', 'customer_phone', 'order_date', 'status', 'total_price', 'products']
