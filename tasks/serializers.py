from django.core.exceptions import ValidationError as DjangoValidationError

from rest_framework import serializers

from .models import TaskCard, Task
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

class TaskCardSerializer(serializers.ModelSerializer):
    class Meta:
        model = TaskCard
        fields = ['id', 'slug', 'title', 'visibility', 'created_at', 'last_updated', 'owner']
        read_only_fields = ['slug', 'created_at', 'last_updated', 'owner']



class TaskSerializer(serializers.ModelSerializer, DeadlineValidationMixin):
    class Meta:
        model = Task
        fields = ['id', 'title', 'description', 'created_at', 'created_by', 'priority', 'deadline',
                  'completed']
        read_only_fields = ['created_by']


class TaskUpdateSerializer(serializers.ModelSerializer, DeadlineValidationMixin):
    class Meta:
        model = Task
        fields = ['title', 'description', 'created_at', 'priority', 'deadline', 'completed']



