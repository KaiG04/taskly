from django.db import models
from django.conf import settings
from django.utils.text import slugify

import secrets

from tasks.validators import validate_deadline


# Create your models here.
class TaskBoard(models.Model):
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
    PRIORITY_LOW = 'L'
    PRIORITY_MEDIUM = 'M'
    PRIORITY_HIGH = 'H'
    PRIORITY_CHOICES = [
        (PRIORITY_LOW, 'Low priority'),
        (PRIORITY_MEDIUM, 'Medium priority'),
        (PRIORITY_HIGH, 'High priority'),
    ]
    title = models.CharField(max_length=255)
    slug = models.SlugField(max_length=255, unique=True)
    description = models.TextField(null=True, blank=True)
    created_at = models.DateTimeField(auto_now_add=True)
    deadline = models.DateTimeField(validators=[validate_deadline], null=True, blank=True)
    priority = models.CharField(max_length=1, choices=PRIORITY_CHOICES, null=True, blank=True)
    created_by = models.ForeignKey(settings.AUTH_USER_MODEL, on_delete=models.CASCADE)
    completed = models.BooleanField(default=False)
    task_board = models.ForeignKey(TaskBoard, on_delete=models.CASCADE, related_name='tasks')

    def save(self, *args, **kwargs):
        if not self.slug or self.title_changed(): # if slug is None, or if title has changed update slug
            self.slug = slugify(f"{self.pk}-{self.title}")
        super().save(*args, **kwargs)

    def title_changed(self):
        """Check if the title has changed."""
        if self.pk:
            old_title = Task.objects.get(pk=self.pk).title
            return old_title != self.title
        return False

    def __str__(self):
        return self.title






