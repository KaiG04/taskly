from rest_framework import serializers

from .models import Task, Category


class TaskSerializer(serializers.ModelSerializer):
    class Meta:
        model = Task
        fields = ['id', 'title', 'description', 'created_at', 'user', 'category', 'priority', 'deadline']
        read_only_fields = ['user']


class CategorySerializer(serializers.ModelSerializer):
    class Meta:
        model = Category
        fields = ['id', 'title', 'description', 'user']
