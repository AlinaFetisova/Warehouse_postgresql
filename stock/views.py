from django.shortcuts import render
from rest_framework import viewsets, status, permissions
from .models import Category, Product
from .serializers import CategorySerializer, ProductSerializer
from rest_framework.filters import SearchFilter, OrderingFilter
from django_filters.rest_framework import DjangoFilterBackend

from rest_framework.decorators import action
from rest_framework.response import Response


# Create your views here.
class CategoryViewSet(viewsets.ModelViewSet):
    queryset=Category.objects.all()
    serializer_class=CategorySerializer
    permission_classes=[permissions.IsAuthenticatedOrReadOnly]

class ProductViewSet(viewsets.ModelViewSet):
    queryset=Product.objects.all()
    serializer_class=ProductSerializer
    permission_classes = [permissions.IsAuthenticatedOrReadOnly]

    filter_backends=[DjangoFilterBackend, SearchFilter, OrderingFilter]
    filterset_fields=['category']
    search_fields=['name', 'sku']
    ordering_fields=['price', 'quantity', 'created_at']

    @action(detail=True, methods=['post'])
    def reduce_stock(self, request, pk=None):
        product=self.get_object()
        quantity_to_reduce=request.data.get('quantity', 0)
        try:
            quantity_to_reduce=int(quantity_to_reduce)
        except(ValueError, TypeError):
            return Response(
                {'error': 'Введіть коректну кількість товару(має бути ціле число)'},
                status=status.HTTP_400_BAD_REQUEST
                )
        
        if (quantity_to_reduce<=0):
            return Response(
                {'error': 'Кількість для списання має бути більшою за 0'},
                status=status.HTTP_400_BAD_REQUEST
            )
        
        if (product.quantity<quantity_to_reduce):
            return Response(
                {'error': f'Недостатньо товару на складі. Доступно лише: {product.quantity} шт.'},
                status=status.HTTP_400_BAD_REQUEST
            )
        
        product.quantity-=quantity_to_reduce
        product.save()
        return Response(
                {'message': 'Успішно списано!'},
                status=status.HTTP_200_OK
            )

