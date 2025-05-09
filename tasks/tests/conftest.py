from datetime import timedelta

import pytest
from django.contrib.auth import get_user_model
from django.utils.timezone import now
from model_bakery import baker
from rest_framework.test import APIClient

from celery.contrib.testing.app import setup_default_app
from celery.contrib.testing.worker import start_worker



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
        created_by=user, # Test user
    )
    data = {
        "title": task.title,
        "slug": task.slug,
        'local_id': task.local_id,
    }
    if task.priority:
        data["priority"] = task.priority
    if task.deadline:
        data["deadline"] = task.deadline.isoformat()
    if task.description:
        data["description"] = task.description
    return data

@pytest.fixture
def valid_board_data(user):
    task_board = baker.make(
        "TaskBoard",  # Task model
        owner=user
    )
    data = {
        "title": task_board.title,
        "slug": task_board.slug,
        "visibility": task_board.visibility,
        "owner": task_board.owner.username,
    }
    if task_board.created_at:
        data["created_at"] = task_board.created_at.isoformat()
    return data

@pytest.fixture
def board_slug(valid_board_data):
    return valid_board_data["slug"]

@pytest.fixture
def created_task_board(user):
    task_board = baker.make(
        "TaskBoard",
        owner=user
    )
    return task_board


@pytest.fixture
def create_task(created_task_board):
    dl = now() + timedelta(hours=23)
    def _bake_task(reminder_notification=False, completed=False, deadline=dl, **kwargs):
        return baker.make(
            "Task",
            created_by=created_task_board.owner,
            task_board=created_task_board,
            deadline=deadline,
            reminder_notification=reminder_notification,
            completed=completed,
            **kwargs,  # Allows overriding additional fields dynamically
        )
    return _bake_task

@pytest.fixture
def action_user():
    User = get_user_model()
    return User.objects.create_user(username='actionuser', password='actionpassword', email="action-user@example.com")




