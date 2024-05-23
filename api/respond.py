from rest_framework.response import Response
from rest_framework.serializers import ModelSerializer
from rest_framework import status
from .helpers import get_or_none
from . import models, serializers


class Respond:
    @staticmethod
    def with_created(serializer_cls, payload):
        serializer = serializer_cls(data=payload)
        if serializer.is_valid():
            serializer.save()
            return Response(serializer.data, status=status.HTTP_201_CREATED)
        return Response(serializer.errors, status=status.HTTP_422_UNPROCESSABLE_ENTITY)

    @staticmethod
    def with_all(model_cls, serial: type[ModelSerializer]):
        serializer = serial(model_cls.objects.all(), many=True)
        return Response(serializer.data, status=status.HTTP_200_OK)

    @classmethod
    def _resource_params(cls, name, pk):
        resource = cls._query_resource(name, pk)
        serializer = getattr(serializers, f'{name}Serializer')
        return [resource, serializer]

    @staticmethod
    def _query_resource(name, pk):
        resource_cls = getattr(models, name)
        return get_or_none(resource_cls, pk=pk)

    @classmethod
    def with_resource(cls, resource_name, pk):
        resource, resource_serializer = cls._resource_params(resource_name, pk)
        if resource:
            serializer = resource_serializer(resource)
            return Response(serializer.data, status=status.HTTP_200_OK)
        return Response(f'<{resource_name} id={pk}> Not Found', status=status.HTTP_404_NOT_FOUND)

    @classmethod
    def with_update(cls, resource_name, update, pk):
        resource, resource_serializer = cls._resource_params(resource_name, pk)
        if resource is None:
            return Response(f'<{resource_name} id={pk}> Not Found', status=status.HTTP_404_NOT_FOUND)

        serializer = resource_serializer(instance=resource, data=update, partial=True)
        if serializer.is_valid():
            serializer.save()
            return Response(serializer.data, status=status.HTTP_200_OK)
        return Response(serializer.errors, status=status.HTTP_422_UNPROCESSABLE_ENTITY)

    @classmethod
    def with_destroy(cls, resource_name, pk):
        resource = cls._query_resource(resource_name, pk)
        if resource:
            resource.delete()
            return Response(f'<{resource_name} id={pk}> successfully deleted', status=status.HTTP_200_OK)
        return Response(f'<{resource_name} id={pk}> Not Found', status=status.HTTP_404_NOT_FOUND)
