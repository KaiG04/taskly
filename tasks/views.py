from django.shortcuts import render
from rest_framework.filters import SearchFilter, OrderingFilter
from rest_framework.permissions import IsAuthenticated, AllowAny
from rest_framework.viewsets import ModelViewSet
from rest_framework.permissions import SAFE_METHODS
from django_filters.rest_framework import DjangoFilterBackend
from django.utils.text import slugify

from .models import Task, TaskCard
from .permissions import IsOwnerOrReadOnly
from .serializers import TaskSerializer, TaskUpdateSerializer, TaskCardSerializer


# Create your views here.
class TaskCardViewSet(ModelViewSet):
    queryset = TaskCard.objects.all()
    serializer_class = TaskCardSerializer
    lookup_field = "slug"


    def perform_create(self, serializer):
        serializer.save(owner=self.request.user)

class TaskViewSet(ModelViewSet):
    queryset = Task.objects.all()
    permission_classes = [IsAuthenticated, IsOwnerOrReadOnly]
    filter_backends = [DjangoFilterBackend, SearchFilter, OrderingFilter]
    lookup_field = 'slug'
    search_fields = ['title']
    ordering_fields = ['created_at']
    http_method_names = ['get', 'post', 'put', 'patch', 'delete']

    def get_serializer_class(self):
        if self.request.method in SAFE_METHODS or self.request.method == 'POST':
            return TaskSerializer
        elif self.request.method == 'PUT' or self.request.method == 'PATCH':
            return TaskUpdateSerializer



    def perform_create(self, serializer):
        task_card = TaskCard.objects.get(slug=self.kwargs['card_slug'])
        task = serializer.save(created_by=self.request.user, task_card=task_card)

        task.slug = slugify(f"{task.id}-{task.title}")
        task.save()


