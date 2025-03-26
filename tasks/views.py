from django.shortcuts import render
from rest_framework.permissions import IsAuthenticated, AllowAny
from rest_framework.viewsets import ModelViewSet

from .models import Task, Category
from .serializers import TaskSerializer, CategorySerializer


# Create your views here.
class TaskViewSet(ModelViewSet):
    serializer_class = TaskSerializer
    permission_classes = [IsAuthenticated]

    def get_queryset(self):
        return Task.objects.select_related('category').filter(user=self.request.user)


    def perform_create(self, serializer):
        serializer.save(user=self.request.user)



class CategoryViewSet(ModelViewSet):
    queryset = Category.objects.all()
    serializer_class = CategorySerializer
