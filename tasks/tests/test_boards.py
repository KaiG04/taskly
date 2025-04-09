import pytest
from django.contrib.auth import get_user_model
from model_bakery import baker
from rest_framework import status

from tasks.models import TaskBoard


@pytest.mark.django_db
class TestGetTaskBoards:

    class TestGetTaskBoardList:
        def test_if_user_is_anonymous_return_401(self, user, api_client):
            """
            Test that the user is authenticated in order to access the task board.
            :param user:
            :param api_client:
            """
            response = api_client.get(f'/{user.username}/boards/')

            assert response.status_code == status.HTTP_401_UNAUTHORIZED

        def test_if_user_is_authorised_return_200(self, user, api_client):
            """
            Test that the user is authenticated in order to access the task board.
            :param user:
            :param api_client:
            """
            api_client.force_authenticate(user=user)

            response = api_client.get(f'/{user.username}/boards/')

            assert response.status_code == status.HTTP_200_OK

        def test_if_user_is_authenticated_and_if_changes_url_gets_redirected_returns_302(self, user, api_client):
            """
            Test that if the user is authenticated, and trys to access another task board by changing the url gets
            redirected to their task board and receives 302.
            :param user:
            :param api_client:
            """
            api_client.force_authenticate(user=user)
            target_username = "bob"

            response = api_client.get(f'/{target_username}/boards/')

            assert response.status_code == status.HTTP_302_FOUND

    class TestGetTaskBoardInstance:
        def test_if_user_is_anonymous_cannot_retrieve_task_board_instance_returns_401(self
                                                                                 , user, api_client, valid_board_data):
            """
            Test that the user is anonymous, and cannot retrieve task board instance.
            :param user:
            :param api_client:
            :param valid_board_data:
            """
            api_client.post(f'/{valid_board_data["owner"]}/boards/', data=valid_board_data)

            response = api_client.get(f'/{valid_board_data["owner"]}/boards/{valid_board_data["slug"]}/')

            assert response.status_code == status.HTTP_401_UNAUTHORIZED

        def test_if_user_is_authenticated_can_retrieve_task_board_instance_returns_200(self,
                                                                                     user, api_client, valid_board_data):
            """
            Test that the user is authenticated, and can retrieve task board instance.
            :param user:
            :param api_client:
            :param valid_board_data:
            """
            api_client.force_authenticate(user=user)
            api_client.post(f'/{valid_board_data["owner"]}/boards/', data=valid_board_data)

            response = api_client.get(f'/{valid_board_data["owner"]}/boards/{valid_board_data["slug"]}/')

            assert response.status_code == status.HTTP_200_OK


