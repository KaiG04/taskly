from django.db import models
from django.conf import settings



# Create your models here.
class Category(models.Model):
    title = models.CharField(max_length=255)
    description = models.TextField(null=True, blank=True)
    user = models.ForeignKey(settings.AUTH_USER_MODEL, on_delete=models.CASCADE)

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
    created_at = models.DateTimeField(auto_now_add=True)
    description = models.TextField(null=True, blank=True)
    deadline = models.DateTimeField(null=True, blank=True)
    priority = models.CharField(max_length=1, choices=PRIORITY_CHOICES, default=PRIORITY_NONE)
    category = models.ForeignKey(Category, on_delete=models.PROTECT, null=True, blank=True)
    user = models.ForeignKey(settings.AUTH_USER_MODEL, on_delete=models.CASCADE)




