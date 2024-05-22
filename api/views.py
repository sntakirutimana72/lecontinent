from rest_framework import views, status
from rest_framework.response import Response
from .serializers import ProductSerializer, OrderSerializer
from .models import Product, Order
from .helpers import get_or_none


class ProductIndexView(views.APIView):
    def get(self, request, *args, **kwargs):
        products = Product.objects.all()
        serializer = ProductSerializer(products, many=True)
        return Response(serializer.data, status=status.HTTP_200_OK)

    def post(self, request, *args, **kwargs):
        serializer = ProductSerializer(data=request.data)
        if serializer.is_valid():
            serializer.save()
            return Response(serializer.data, status=status.HTTP_201_CREATED)
        return Response(serializer.errors, status=status.HTTP_422_UNPROCESSABLE_ENTITY)


class ProductDetailView(views.APIView):
    @staticmethod
    def _queryset(pk):
        return get_or_none(Product, pk=pk)

    def get(self, request, pk):
        product = self._queryset(pk)
        if product is None:
            return Response('No product found', status=status.HTTP_404_NOT_FOUND)
        return Response(ProductSerializer(product).data)

    def put(self, request, pk):
        product = self._queryset(pk)
        if product is None:
            return Response(f'Product with id={pk} not found', status=status.HTTP_404_NOT_FOUND)

        serializer = ProductSerializer(instance=product, data=request.data, partial=True)
        if serializer.is_valid():
            serializer.save()
            return Response(serializer.data, status=status.HTTP_200_OK)
        return Response(serializer.errors, status=status.HTTP_422_UNPROCESSABLE_ENTITY)

    def delete(self, request, pk):
        product = self._queryset(pk)
        if product is None:
            return Response(f'Product with id={pk} not found', status=status.HTTP_404_NOT_FOUND)
        product.delete()
        return Response(f'Product with id = {pk} has been successfully deleted', status=status.HTTP_200_OK)


class OrderIndexView(views.APIView):
    def get(self, request, *args, **kwargs):
        orders = Order.objects.all()
        serializer = OrderSerializer(orders, many=True)
        return Response(serializer.data, status=status.HTTP_200_OK)

    def post(self, request, *args, **kwargs):
        serializer = OrderSerializer(data=request.data)
        if serializer.is_valid():
            serializer.save()
            return Response(serializer.data, status=status.HTTP_201_CREATED)
        return Response(serializer.errors, status=status.HTTP_422_UNPROCESSABLE_ENTITY)


class OrderDetailView(views.APIView):
    @staticmethod
    def _queryset(pk):
        return get_or_none(Order, pk=pk)

    def get(self, request, pk):
        order = self._queryset(pk)
        if order is None:
            return Response('No order found', status=status.HTTP_404_NOT_FOUND)
        return Response(ProductSerializer(order).data, status=status.HTTP_200_OK)

    def put(self, request, pk):
        order = self._queryset(pk)
        if order is None:
            return Response(f'Order with id={pk} not found', status=status.HTTP_404_NOT_FOUND)

        serializer = ProductSerializer(instance=order, data=request.data, partial=True)
        if serializer.is_valid():
            serializer.save()
            return Response(serializer.data, status=status.HTTP_200_OK)
        return Response(serializer.errors, status=status.HTTP_422_UNPROCESSABLE_ENTITY)

    def delete(self, request, pk):
        order = self._queryset(pk)
        if order is None:
            return Response(f'Order with id={pk} not found', status=status.HTTP_404_NOT_FOUND)
        order.delete()
        return Response(f'Order with id = {pk} has been successfully deleted', status=status.HTTP_200_OK)
