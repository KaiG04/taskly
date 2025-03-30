from rest_framework import serializers

from .models import Task, Category


class TaskSerializer(serializers.ModelSerializer):
    class Meta:
        model = Task
        fields = ['id', 'title', 'description', 'created_at', 'created_by', 'category', 'priority', 'deadline']
        read_only_fields = ['created_by']


class CategorySerializer(serializers.ModelSerializer):
    class Meta:
        model = Category
        fields = ['id', 'title', 'description', 'created_by']
