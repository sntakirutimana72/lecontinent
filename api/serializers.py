from rest_framework import serializers
from .models import Product, Order


class ProductSerializer(serializers.ModelSerializer):
    class Meta:
        model = Product
        fields = ['id', 'name', 'description', 'price', 'stock', 'created_at', 'updated_at']


class OrderSerializer(serializers.ModelSerializer):
    products = ProductSerializer(source='order.products', read_only=True, many=True)

    class Meta:
        model = Order
        fields = ['id', 'customer_name', 'customer_phone', 'order_date', 'status', 'total_price', 'products']
