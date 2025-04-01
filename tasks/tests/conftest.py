from unicodedata import category

import pytest
from django.contrib.auth import get_user_model
from model_bakery import baker
from rest_framework.test import APIClient

from tasks.models import Category


@pytest.fixture
def user():
    User = get_user_model()
    return User.objects.create_user(username='testuser', password='testpassword', email="testuser@example.com")

@pytest.fixture
def api_client():
    return APIClient()


@pytest.fixture
def valid_task_data(user):
    task = baker.prepare(
        "Task",  # Task model
        created_by=user # Test user
    )
    data = {
        "title": task.title,
        "priority": task.priority,
    }
    if task.category:
        data["category"] = task.category.id
    if task.deadline:
        data["deadline"] = task.deadline.isoformat()
    if task.description:
        data["description"] = task.description
    return data