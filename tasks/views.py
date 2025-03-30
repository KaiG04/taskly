from django.shortcuts import render
from rest_framework.filters import SearchFilter, OrderingFilter
from rest_framework.permissions import IsAuthenticated, AllowAny
from rest_framework.viewsets import ModelViewSet
from django_filters.rest_framework import DjangoFilterBackend

from .models import Task, Category
from .serializers import TaskSerializer, CategorySerializer


# Create your views here.
class TaskViewSet(ModelViewSet):
    serializer_class = TaskSerializer
    permission_classes = [IsAuthenticated]
    filter_backends = [DjangoFilterBackend, SearchFilter, OrderingFilter]
    filterset_fields = ['category']
    search_fields = ['title']
    ordering_fields = ['created_at']

    def get_queryset(self):
        queryset = Task.objects.all()
        user = self.request.user
        if user.is_authenticated:
            queryset = queryset.filter(created_by=user)
        return queryset

    def perform_create(self, serializer):
        serializer.save(created_by=self.request.user)



class CategoryViewSet(ModelViewSet):
    queryset = Category.objects.all()
    serializer_class = CategorySerializer
