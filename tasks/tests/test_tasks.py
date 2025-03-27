import pytest

from rest_framework import status
from rest_framework.test import APIClient



@pytest.mark.django_db
class TestGetTask:
    def test_if_user_is_anonymous_returns_401(self):

        client = APIClient()
        response = client.get('/tasks/')

        assert response.status_code == status.HTTP_401_UNAUTHORIZED


    def test_if_user_is_authenticated_returns_200(self, user):
        client = APIClient()

        client.force_authenticate(user=user)

        response = client.get('/tasks/')

        assert response.status_code == status.HTTP_200_OK

    def test_if_user_is_admin_returns_200(self, user):
        client = APIClient()

        user.is_staff = True
        user.save()
        client.force_authenticate(user=user)
        response = client.get('/tasks/')

        assert response.status_code == status.HTTP_200_OK

