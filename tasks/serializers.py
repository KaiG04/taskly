from django.core.exceptions import ValidationError as DjangoValidationError

from rest_framework import serializers

from .models import Task, Category
from .validators import validate_deadline


class DeadlineValidationMixin:
    """Mixin to reuse the deadline validation across multiple serializers."""
    def validate_deadline(self, value):
        """Reusing the model validation and converting Django errors to DR errors."""
        try:
            validate_deadline(value)
        except DjangoValidationError as e:
            raise serializers.ValidationError(e.messages) # Convert Django error to DRF error
        return value


class TaskSerializer(serializers.ModelSerializer, DeadlineValidationMixin):
    class Meta:
        model = Task
        fields = ['id', 'title', 'description', 'created_at', 'created_by', 'category', 'priority', 'deadline']
        read_only_fields = ['created_by']


class TaskUpdateSerializer(serializers.ModelSerializer, DeadlineValidationMixin):
    class Meta:
        model = Task
        fields = ['title', 'description', 'created_at', 'category', 'priority', 'deadline']


class CategorySerializer(serializers.ModelSerializer):
    class Meta:
        model = Category
        fields = ['id', 'title', 'description', 'created_by']
