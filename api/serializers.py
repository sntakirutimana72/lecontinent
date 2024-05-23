from rest_framework import serializers
from .models import Product, Order


class ProductSerializer(serializers.ModelSerializer):
    class Meta:
        model = Product
        fields = '__all__'


class OrderSerializer(serializers.ModelSerializer):
    class Meta:
        model = Order
        fields = '__all__'

    def to_representation(self, instance):
        obj = super().to_representation(instance)
        prod_ids = obj['products']
        obj['products'] = ProductSerializer(Product.objects.filter(id__in=prod_ids), many=True).data
        return obj
