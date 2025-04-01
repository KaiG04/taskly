from datetime import timedelta

import pytest
from model_bakery import baker

from django.utils.timezone import now

from rest_framework import status

from tasks.models import Task


@pytest.mark.django_db
class TestGetTask:
    def test_if_user_is_anonymous_returns_401(self, api_client):
        """
        Test that the user must be authenticated to access tasks page and receives 401 response.
        :param api_client:
        """

        response = api_client.get('/tasks/')

        assert response.status_code == status.HTTP_401_UNAUTHORIZED


    def test_if_user_is_authenticated_returns_200(self, user, api_client):
        """
        Test that an authenticated user can access the tasks page and receives a 200 response.
        :param user:
        :param api_client:
        """
        api_client.force_authenticate(user=user)

        response = api_client.get('/tasks/')

        assert response.status_code == status.HTTP_200_OK

    def test_if_user_is_admin_returns_200(self, user, api_client):
        """
        Test that an admin user can access the tasks page and receives a 200 response.
        :param user:
        :param api_client:
        """
        user.is_staff = True
        user.save()
        api_client.force_authenticate(user=user)

        response = api_client.get('/tasks/')

        assert response.status_code == status.HTTP_200_OK
        assert user.is_staff

    def test_if_user_can_retrieve_specific_task_returns_200(self, user, api_client):
        """
        Test that an authenticated user can access a specific task and receives a 200 response.
        :param user:
        :param api_client:
        """
        task = baker.make(Task, created_by=user) #passing created_by as is required, and baker doesn't set this
        api_client.force_authenticate(user=user)

        response = api_client.get(f'/tasks/{task.id}/')

        assert response.status_code == status.HTTP_200_OK



@pytest.mark.django_db
class TestCreateTask:
    def test_if_user_is_anonymous_returns_401(self, valid_task_data, api_client):
        """
        Test that an anonymous user cannot create a new task and receives a 401 response.
        :param valid_task_data:
        """

        response = api_client.post('/tasks/', data=valid_task_data)

        assert response.status_code == status.HTTP_401_UNAUTHORIZED

    def test_if_user_is_admin_returns_201(self, user, valid_task_data, api_client):
        """
        Test that an admin user can create a new task and receives a 201 response.
        :param user:
        :param valid_task_data:
        :param api_client:
        """
        api_client.force_authenticate(user=user)
        user.is_staff = True
        user.save()

        response = api_client.post('/tasks/', data=valid_task_data)

        assert response.status_code == status.HTTP_201_CREATED
        assert user.is_staff



    def test_if_user_is_authenticated_returns_201(self, user, valid_task_data, api_client):
        """
        Test that an authenticated user can create a task and receives a 201 response.
        :param user:
        :param valid_task_data:
        :param api_client:
        """
        api_client.force_authenticate(user=user)

        response = api_client.post('/tasks/', valid_task_data)

        assert response.status_code == status.HTTP_201_CREATED

        assert response.data["title"] == valid_task_data["title"]
        assert response.data["priority"] == valid_task_data["priority"]

        # Assert optional fields only if present in the response
        assert response.data.get("description") == valid_task_data.get("description")
        assert response.data.get("deadline") == valid_task_data.get("deadline")

        # Check if the task was saved in the database
        task = Task.objects.get(id=response.data["id"])
        assert task.title == valid_task_data["title"]
        assert task.priority == valid_task_data["priority"]

    def test_task_is_created_for_correct_user_returns_201(self, user, valid_task_data, api_client):
        """
        Test that the task is correctly associated with the authenticated user and receives a 201 response.
        :param user:
        :param valid_task_data:
        :param api_client:
        """
        api_client.force_authenticate(user=user)

        response = api_client.post('/tasks/', valid_task_data)
        task = Task.objects.get(id=response.data["id"])

        assert response.status_code == status.HTTP_201_CREATED
        assert task.created_by == user

    def test_if_deadline_is_in_past_returns_400(self, user, valid_task_data, api_client):
        """
        Test that the deadline is in the past and receives a 400 response.
        :param user:
        :param valid_task_data:
        :param api_client:
        """
        api_client.force_authenticate(user=user)

        response = api_client.post('/tasks/', data=
        {
            **valid_task_data,
            "deadline": (now() - timedelta(days=1)).isoformat(),
        })

        assert response.status_code == status.HTTP_400_BAD_REQUEST
        assert "deadline" in response.data
        assert isinstance(response.data["deadline"], list) # Checks is type list
        assert response.data["deadline"] # Checks that list is not empty

    def test_if_deadline_is_none_returns_201(self, user, valid_task_data, api_client):
        """
        Test that Task can still be created with no deadline receives 201 response.
        :param user:
        :param valid_task_data:
        :param api_client:
        """
        api_client.force_authenticate(user=user)

        response = api_client.post('/tasks/', data={
            **valid_task_data,
            "deadline": ""
        })

        assert response.status_code == status.HTTP_201_CREATED

    def test_if_deadline_is_in_future_returns_201(self, user, valid_task_data, api_client):
        """
        Test that the deadline is in the future and receives a 201 response.
        :param user:
        :param valid_task_data:
        :param api_client:
        """
        api_client.force_authenticate(user=user)

        response = api_client.post('/tasks/', data={
            **valid_task_data,
            "deadline": (now() + timedelta(days=24)).isoformat(),
        })

        assert response.status_code == status.HTTP_201_CREATED

    def test_if_deadline_is_now_returns_400(self, user, valid_task_data, api_client):
        # Validation only allows creation of object if deadline is null or in the future
        """
        Test that the deadline is exactly now and receives a 400 response.
        :param user:
        :param valid_task_data:
        :param api_client:
        """
        api_client.force_authenticate(user=user)

        response = api_client.post('/tasks/', data={
            **valid_task_data,
            "deadline": now().isoformat(),
        })

        assert response.status_code == status.HTTP_400_BAD_REQUEST
        assert isinstance(response.data["deadline"], list)
        assert response.data["deadline"]

    def test_that_deadline_has_no_limit_returns_201(self, user, valid_task_data, api_client):
        """
        Test that the deadline can be set for many years in the future, has no unintended restrictions,
        and receives a 201 response.
        :param user:
        :param valid_task_data:
        :param api_client:
        """
        api_client.force_authenticate(user=user)

        response = api_client.post('/tasks/', data={
            **valid_task_data,
            "deadline": (now() + timedelta(weeks=52177)).isoformat(), #1000 years in future
        })

        assert response.status_code == status.HTTP_201_CREATED


    def test_if_optional_fields_allow_task_creation_returns_201(self, user, api_client):
        """
        Test that the optional fields for task creation are correctly implemented receives 201 response.
        :param user:
        :param api_client:
        """
        api_client.force_authenticate(user=user)

        response = api_client.post('/tasks/', data={
            "title": "Test Title",
            "priority": "H",
            "description": "Test Description",
            "deadline": (now() + timedelta(days=1)).isoformat() # One day ahead to follow validation rules
        })

        assert response.status_code == status.HTTP_201_CREATED

    def test_if_data_is_invalid_returns_400(self, user, api_client):
        """
        Test that invalid data cannot create a  task and receives a 400 response.
        :param user:
        :param api_client:
        """
        api_client.force_authenticate(user=user)

        response = api_client.post('/tasks/', data={})

        assert response.status_code == status.HTTP_400_BAD_REQUEST

    def test_if_title_is_missing_returns_400(self, user, api_client):
        """
        Test that a missing title cannot create a  task and receives a 400 response.
        :param user:
        :param api_client:
        """
        api_client.force_authenticate(user=user)

        response = api_client.post('/tasks/', data={"priority": "H"})

        assert response.status_code == status.HTTP_400_BAD_REQUEST

@pytest.mark.django_db
class TestUpdateTask:
    def test_if_user_is_anonymous_returns_401(self, api_client):
        """
        Test that an anonymous user cannot update a task and receives a 401 response.
        :param api_client:
        """
        task = baker.make(Task)
        api_client.force_authenticate(user=None)

        response = api_client.put(f'/tasks/{task.id}/', data={"title": "Test Update Title"})

        assert response.status_code == status.HTTP_401_UNAUTHORIZED

    def test_if_user_is_authenticated_can_patch_returns_200(self, user, api_client):
        """
        Test that an authenticated user can partially(patch) update a task and receives a 200 response.
        :param user:
        :param api_client:
        """
        api_client.force_authenticate(user=user)
        task = baker.make(Task, created_by=user)

        response = api_client.put(f'/tasks/{task.id}/', data={"title": "Test Update Title"})

        assert response.status_code == status.HTTP_200_OK
        assert response.data["title"] == "Test Update Title"

    def test_if_user_is_authenticated_can_put_returns_200(self, user, api_client):
        """
        Test that an authenticated user can fully(put) update a task and receives a 200 response.
        :param user:
        :param api_client:
        """
        api_client.force_authenticate(user=user)
        task = baker.make(Task, created_by=user)

        response = api_client.put(f'/tasks/{task.id}/',
        data={
            "title": "Test Update Title",
            "description": "Test Update Description",
            "deadline": (now() + timedelta(days=1)).isoformat(),
            "priority": "H",
        })

        assert response.status_code == status.HTTP_200_OK
        assert response.data["title"] == "Test Update Title"

    def test_if_user_is_admin_returns_200(self, user, api_client):
        """
        Test that an authenticated user can update a task and receives a 200 response.
        :param user:
        :param api_client:
        """
        task = baker.make(Task, created_by=user)
        api_client.force_authenticate(user=user)
        user.is_staff = True
        user.save()

        response = api_client.put(f'/tasks/{task.id}/', data={"title": "Test Update Title"})

        assert response.status_code == status.HTTP_200_OK
        assert response.data["title"] == "Test Update Title"
        assert user.is_staff


    def test_if_data_is_invalid_returns_400(self, user, api_client):
        """
        Test that invalid data cannot update a task and receives a 400 response.
        :param user:
        :param api_client:
        """
        task = baker.make(Task, created_by=user)
        api_client.force_authenticate(user=user)

        response = api_client.put(f'/tasks/{task.id}/', data={"title": ""})

        assert response.status_code == status.HTTP_400_BAD_REQUEST

    def test_non_owners_of_tasks_cannot_update_returns_403(self, user, api_client, django_user_model):
        """
        Test that a user, that did not create the task cannot update the task and receives a 403 response.
        :param user:
        :param api_client:
        :return:
        """
        task_owner = user
        non_owner = django_user_model.objects.create_user(
            username='non_owner_user', password='testpassword', email="non_owner_user@example.com")

        task = baker.make(Task, created_by=task_owner)
        print(task_owner, non_owner)

        api_client.force_authenticate(user=non_owner)

        response = api_client.put(f'/tasks/{task.id}/', data={"title": "newtitle"})

        assert response.status_code == status.HTTP_403_FORBIDDEN


