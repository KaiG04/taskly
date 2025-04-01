from django.db import models
from django.conf import settings

import secrets

from tasks.validators import validate_deadline


# Create your models here.
class TaskCard(models.Model):
    VISIBILITY_PUBLIC = 'PUB'
    VISIBILITY_PRIVATE = 'PRI'
    VISIBILITY_CHOICES = [
        (VISIBILITY_PUBLIC, 'Public'),
        (VISIBILITY_PRIVATE, 'Private'),
    ]
    slug = models.CharField(max_length=12, unique=True, blank=True)
    title = models.CharField(max_length=255)
    visibility = models.CharField(choices=VISIBILITY_CHOICES, max_length=3, default=VISIBILITY_PUBLIC)
    created_at = models.DateTimeField(auto_now_add=True)
    last_updated = models.DateTimeField(auto_now=True)
    owner = models.ForeignKey(settings.AUTH_USER_MODEL, on_delete=models.CASCADE)

    def save(self, *args, **kwargs):
        if not self.slug: # Prevents changing URLs on updates
            self.slug = secrets.token_urlsafe(8)
        super().save(*args, **kwargs)


class Task(models.Model):
    PRIORITY_NONE = 'N'
    PRIORITY_LOW = 'L'
    PRIORITY_MEDIUM = 'M'
    PRIORITY_HIGH = 'H'
    PRIORITY_CHOICES = [
        (PRIORITY_NONE, 'No priority'),
        (PRIORITY_LOW, 'Low priority'),
        (PRIORITY_MEDIUM, 'Medium priority'),
        (PRIORITY_HIGH, 'High priority'),
    ]

    title = models.CharField(max_length=255)
    description = models.TextField(null=True, blank=True)
    created_at = models.DateTimeField(auto_now_add=True)
    deadline = models.DateTimeField(validators=[validate_deadline], null=True, blank=True)
    priority = models.CharField(max_length=1, choices=PRIORITY_CHOICES, default=PRIORITY_NONE)
    created_by = models.ForeignKey(settings.AUTH_USER_MODEL, on_delete=models.CASCADE)
    completed = models.BooleanField(default=False)
    task_card = models.ForeignKey(TaskCard, on_delete=models.CASCADE, related_name='tasks')

    def __str__(self):
        return self.title






