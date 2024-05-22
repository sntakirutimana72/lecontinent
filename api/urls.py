from django.urls import path
from . import views

urlpatterns = [
    path('products/', views.ProductIndexView.as_view(), name='prod-index'),
    path('products/<int:pk>/', views.ProductDetailView.as_view(), name='prod-details'),
    path('orders/', views.OrderIndexView.as_view(), name='order-index'),
    path('orders/<int:pk>/', views.OrderDetailView.as_view(), name='order-details'),
]
