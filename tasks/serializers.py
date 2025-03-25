from rest_framework import serializers

from .models import Task


class TaskSerializer(serializers.ModelSerializer):
    user_id = serializers.IntegerField(read_only=True)

    class Meta:
        model = Task
        fields = ['title', 'description', 'created_at', 'user_id', 'category', 'priority', 'deadline']
