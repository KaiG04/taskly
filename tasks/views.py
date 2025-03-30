from django.shortcuts import render
from rest_framework.filters import SearchFilter, OrderingFilter
from rest_framework.permissions import IsAuthenticated, AllowAny
from rest_framework.viewsets import ModelViewSet
from rest_framework.permissions import SAFE_METHODS
from django_filters.rest_framework import DjangoFilterBackend

from .models import Task, Category
from .serializers import TaskSerializer, CategorySerializer, TaskUpdateSerializer


# Create your views here.
class TaskViewSet(ModelViewSet):
    permission_classes = [IsAuthenticated]
    filter_backends = [DjangoFilterBackend, SearchFilter, OrderingFilter]
    filterset_fields = ['category']
    search_fields = ['title']
    ordering_fields = ['created_at']
    http_method_names = ['get', 'post', 'put', 'patch', 'delete']


    def get_serializer_class(self):
        if self.request.method in SAFE_METHODS or self.request.method == 'POST':
            return TaskSerializer
        elif self.request.method == 'PUT' or self.request.method == 'PATCH':
            return TaskUpdateSerializer

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
