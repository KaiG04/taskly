from django.shortcuts import render
from rest_framework.permissions import IsAuthenticated, AllowAny
from rest_framework.viewsets import ModelViewSet

from .models import Task, Category
from .serializers import TaskSerializer, CategorySerializer


# Create your views here.
class TaskViewSet(ModelViewSet):
    queryset = Task.objects.all()
    serializer_class = TaskSerializer
    permission_classes = [IsAuthenticated]


    def perform_create(self, serializer):
        serializer.save(user=self.request.user)



class CategoryViewSet(ModelViewSet):
    queryset = Category.objects.all()
    serializer_class = CategorySerializer
