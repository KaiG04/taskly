
import pytest
from django.contrib.auth import get_user_model
from model_bakery import baker
from rest_framework.test import APIClient

from tasks.models import TaskBoard


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
    if task.deadline:
        data["deadline"] = task.deadline.isoformat()
    if task.description:
        data["description"] = task.description
    return data

@pytest.fixture
def valid_board_data(user):
    task_board = baker.make(
        "TaskBoard",  # Task model
        owner=user,
    )
    data = {
        "title": task_board.title,
        "slug": task_board.slug,
        "owner": task_board.owner.username,
    }
    return data