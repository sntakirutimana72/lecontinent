from rest_framework import views
from .respond import Respond
from .serializers import ProductSerializer, OrderSerializer
from .models import Product, Order


class BaseDetailView(views.APIView):
    resource_name: str

    def get(self, _, pk):
        return Respond.with_resource(self.resource_name, pk)

    def put(self, request, pk):
        return Respond.with_update(self.resource_name, request.data, pk)

    def delete(self, _, pk):
        return Respond.with_destroy(self.resource_name, pk)


class BaseIndexView(views.APIView):
    serializer_cls: type[OrderSerializer | ProductSerializer]
    resource_cls: type[Order | Product]

    def get(self, _):
        return Respond.with_all(self.resource_cls, self.serializer_cls)

    def post(self, request):
        return Respond.with_created(self.serializer_cls, request.data)


# noinspection PyMethodMayBeStatic
class ProductIndexView(BaseIndexView):
    resource_cls = Product
    serializer_cls = ProductSerializer


class ProductDetailView(BaseDetailView):
    resource_name = 'Product'


# noinspection PyMethodMayBeStatic
class OrderIndexView(BaseIndexView):
    resource_cls = Order
    serializer_cls = OrderSerializer


class OrderDetailView(BaseDetailView):
    resource_name = 'Order'
