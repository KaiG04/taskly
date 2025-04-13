import threading

import pytest
from django.contrib.auth import get_user_model

from rest_framework import status


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
            assert response.url == f'/{user.username}/boards/'

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

        def test_if_user_is_authenticated_and_if_changes_url_gets_redirected_returns_302(
                self, user, api_client, valid_board_data):
            """
            Test that a user is authenticated in order to access the task board instance. If the user tries to
            manipulate the url by changing the username. It will auto-redirect the user back to their username
            :param user:
            :param api_client:
            :param valid_board_data:
            """
            api_client.force_authenticate(user=user)
            api_client.post(f'/{valid_board_data["owner"]}/boards/', data=valid_board_data)
            changed_username = 'bob'

            response = api_client.get(f'/{changed_username}/boards/{valid_board_data["slug"]}/')

            assert response.status_code == status.HTTP_302_FOUND
            assert response.url == f'/{valid_board_data["owner"]}/boards/{valid_board_data["slug"]}/'

        def test_if_user_provides_invalid_task_board_slug_returns_404(self, user, api_client, valid_board_data):
            """
            Test that if the user provides a slug for a board that does not exist, it will return 404.
            :param user:
            :param api_client:
            :param valid_board_data:
            """
            api_client.force_authenticate(user=user)
            api_client.post(f'/{valid_board_data["owner"]}/boards/', data=valid_board_data)
            invalid_slug = 'smiler'

            response = api_client.get(f'/{valid_board_data["owner"]}/boards/{invalid_slug}/')

            assert response.status_code == status.HTTP_404_NOT_FOUND

        def test_user_cannot_retrieve_task_board_instance_they_do_not_own_redirects_returns_302(self, user, api_client,
                                                                                      valid_board_data):
            """
            Test that the user is authenticated, and cannot retrieve task board instance they do not own.
            Redirects user to their own task board instance. Returns 302
            :param user:
            :param api_client:
            :param valid_board_data:
            :return:
            """
            User = get_user_model()
            fake_user = User.objects.create_user(username='fakeuser', password='testpassword', email="fakeuser@example.com")
            api_client.force_authenticate(user=fake_user)
            api_client.post(f'/{user.username}/boards/', data=valid_board_data)

            response = api_client.get(f'/{user.username}/boards/{valid_board_data["slug"]}/')

            assert response.status_code == status.HTTP_302_FOUND


@pytest.mark.django_db
class TestPostTaskBoard:
    def test_if_user_is_anonymous_cannot_post_task_board_returns_401(self, user, api_client, valid_board_data):
        """
        Test that the user is anonymous, and cannot post task board instance returned 401.
        :param user:
        :param api_client:
        :param valid_board_data:
        """
        response = api_client.post(f'/{user.username}/boards/', data=valid_board_data)

        assert response.status_code == status.HTTP_401_UNAUTHORIZED

    def test_if_user_is_authenticated_can_post_valid_data_to_task_board_returns_201(self,
                                                                                    user, api_client, valid_board_data):
        """
        Test that the user is authenticated, and can post valid data to the task board instance returned 201.
        :param user:
        :param api_client:
        :param valid_board_data:
        """
        api_client.force_authenticate(user=user)

        response = api_client.post(f'/{user.username}/boards/', data=valid_board_data)

        assert response.status_code == status.HTTP_201_CREATED
        assert response.data["title"] == valid_board_data["title"]
        assert response.data["visibility"] == valid_board_data["visibility"]
        assert response.data["owner"] == user.id

    def test_that_user_cannot_create_task_board_without_title_returns_400(self, user, api_client, valid_board_data):
        """
        Test that the user is authenticated, and cannot create task board without title. Returns 400.
        :param user:
        :param api_client:
        :param valid_board_data:
        """
        api_client.force_authenticate(user=user)

        response = api_client.post(f'/{user.username}/boards/', data={
            **valid_board_data,
            "title": ''
        })

        assert response.status_code == status.HTTP_400_BAD_REQUEST

    def test_that_slug_is_auto_created_with_task_board_creation_returns_201(self, user, api_client, valid_board_data):
        """
        Test that the user is authenticated, and the task board slug is automatically created
         with valid task board creation, returns 201.
        :param user:
        :param api_client:
        :param valid_board_data:
        """
        api_client.force_authenticate(user=user)

        response = api_client.post(f'/{user.username}/boards/', data={
            "title": valid_board_data["title"],
        })

        assert response.status_code == status.HTTP_201_CREATED
        assert "slug" in response.data
        assert response.data["slug"]

    def test_if_user_passes_invalid_optional_field_returns_400(self, user, api_client, valid_board_data):
        """
        Test that the user is authenticated, and if the user passes an invalid option, it will return 400.
        :param user:
        :param api_client:
        :param valid_board_data:
        """
        api_client.force_authenticate(user=user)

        response = api_client.post(f'/{user.username}/boards/', data={
            **valid_board_data,
            "visibility": 'INVALID'
        })

        assert response.status_code == status.HTTP_400_BAD_REQUEST

    def test_if_duplicate_title_a_unique_slug_is_created_returns_201(self, user, api_client, valid_board_data):
        """
        Test that the user is authenticated, if the user creates multiple task boards with the same title,
        the slugs are unique. Returns 201.
        :param user:
        :param api_client:
        :param valid_board_data:
        """
        api_client.force_authenticate(user=user)

        response = api_client.post(f'/{user.username}/boards/', data={
            **valid_board_data,
            'title': 'hello world'
        })
        response2 = api_client.post(f'/{user.username}/boards/', data={
            **valid_board_data,
            'title': 'hello world'
        })

        assert response.status_code == status.HTTP_201_CREATED
        assert response.data['slug'] != response2.data['slug']

    def test_visibility_field_only_allows_choices_options_returns_400(self, user, api_client, valid_board_data):
        """
        Test that the user is authenticated, and the task board visibility field is only allowed to be our custom
        choices. Returns 400.
        :param user:
        :param api_client:
        :param valid_board_data:
        :return:
        """
        api_client.force_authenticate(user=user)
        invalid_data = {
            **valid_board_data,
            "visibility": "INVALID",
        }

        response = api_client.post(f'/{user.username}/boards/', data=invalid_data)

        assert response.status_code == status.HTTP_400_BAD_REQUEST
        assert "visibility" in response.data


@pytest.mark.django_db
class TestPutPatchTaskBoard:
    def test_if_user_is_anonymous_cannot_put_patch_task_board_returns_401(self, user, api_client, valid_board_data):
        """
        Test that the user is anonymous, and cannot put/patch task board instance returned 401.
        :param user:
        :param api_client:
        :param valid_board_data:
        """
        api_client.force_authenticate(user=user)
        api_client.post(f'/{user.username}/boards/', data=valid_board_data)
        api_client.logout()

        response = api_client.patch(f'/{valid_board_data["owner"]}/boards/{valid_board_data["slug"]}/', data={
            "title": 'hello world'
        })

        assert response.status_code == status.HTTP_401_UNAUTHORIZED

    def test_if_user_is_authenticated_can_patch_task_board_returns_200(self, user, api_client, valid_board_data):
        """
        Test that the user is authenticated, and can patch their task board instance returned 200.
        :param user:
        :param api_client:
        :param valid_board_data:
        :return:
        """
        api_client.force_authenticate(user=user)
        api_client.post(f'/{user.username}/boards/', data=valid_board_data)

        response = api_client.patch(f'/{user.username}/boards/{valid_board_data["slug"]}/', data={
            "title": 'hello world'
        })

        assert response.status_code == status.HTTP_200_OK
        assert response.data['title'] != valid_board_data["title"]

    def test_if_user_is_authenticated_can_put_task_board_returns_200(self, user, api_client, valid_board_data):
        """
        Test that the user is authenticated, and can put their task board instance returned 200.
        :param user:
        :param api_client:
        :param valid_board_data:
        :return:
        """
        api_client.force_authenticate(user=user)
        api_client.post(f'/{user.username}/boards/', data=valid_board_data)

        response = api_client.put(f'/{user.username}/boards/{valid_board_data["slug"]}/', data={
            "title": 'hello world',
            "visibility": 'PRI'
        })

        assert response.status_code == status.HTTP_200_OK
        assert response.data['title'] != valid_board_data["title"]

    def test_if_user_patch_and_passes_invalid_field_returns_400(self, user, api_client, valid_board_data):
        """
        Test that the user is authenticated, if the user passes an invalid option, it will return 400.
        :param user:
        :param api_client:
        :param valid_board_data:
        :return:
        """
        api_client.force_authenticate(user=user)
        api_client.post(f'/{user.username}/boards/', data=valid_board_data)

        response = api_client.patch(f'/{user.username}/boards/{valid_board_data["slug"]}/', data={
            "title": '',
        })

        assert response.status_code == status.HTTP_400_BAD_REQUEST

    def test_if_user_puts_and_passes_invalid_field_returns_400(self, user, api_client, valid_board_data):
        """
        Test that the user is authenticated, if the user passes an invalid option, it will return 400.
        :param user:
        :param api_client:
        :param valid_board_data:
        :return:
        """
        api_client.force_authenticate(user=user)
        api_client.post(f'/{user.username}/boards/', data=valid_board_data)

        response = api_client.put(f'/{user.username}/boards/{valid_board_data["slug"]}/', data={
            "title": '',
        })

        assert response.status_code == status.HTTP_400_BAD_REQUEST

    def test_if_user_put_requests_with_all_read_only_fields_changed_returns_200(self, user, api_client, valid_board_data):
        """
        Test that the user is authenticated, if the user sends a put request with all read only fields 'changed' the
        database should NOT be updated with these fields as they are read-only. Returns 200.
        :param user:
        :param api_client:
        :param valid_board_data:
        :return:
        """
        api_client.force_authenticate(user=user)
        api_client.put(f'/{user.username}/boards/', data=valid_board_data)

        invalid_data = {
                "id": 9876316873168731,
                "slug": "notavalidslug",
                "title": "updated board",
                "visibility": "PUB",
                "created_at": "blahblahblah",
                "last_updated": "blooblahblah",
                "owner": 198765,
        }


        response = api_client.put(f'/{user.username}/boards/{valid_board_data["slug"]}/', data={**invalid_data})

        assert response.status_code == status.HTTP_200_OK
        assert response.data['id'] !=  invalid_data['id']
        assert response.data['slug'] != invalid_data['slug']
        assert response.data['created_at'] != invalid_data['created_at']
        assert response.data['last_updated'] != invalid_data['last_updated']
        assert response.data['owner'] != invalid_data['owner']

@pytest.mark.django_db
class TestDeleteTaskBoard:
    def test_if_user_is_anonymous_cannot_delete_task_board_returns_401(self, user, api_client, valid_board_data):
        """
        Test that the user is anonymous, the user cannot delete task board returns 401.
        :param user:
        :param api_client:
        :param valid_board_data:
        :return:
        """
        api_client.force_authenticate(user=user)
        api_client.post(f'/{user.username}/boards/', data=valid_board_data)
        api_client.logout()

        response = api_client.delete(f'/{user.username}/boards/{valid_board_data["slug"]}/')

        assert response.status_code == status.HTTP_401_UNAUTHORIZED

    def test_if_user_is_authenticated_and_is_task_board_owner_can_delete_task_board_returns_204(
            self, user, api_client, valid_board_data):
        """
        Test that the user is authenticated, and is owner, can delete task board returns 204.
        :param user:
        :param api_client:
        :param valid_board_data:
        :return:
        """
        api_client.force_authenticate(user=user)
        api_client.post(f'/{user.username}/boards/', data=valid_board_data)

        response = api_client.delete(f'/{user.username}/boards/{valid_board_data["slug"]}/')

        assert response.status_code == status.HTTP_204_NO_CONTENT
        assert api_client.get(f'/{user.username}/boards/{valid_board_data["slug"]}/').status_code == 404

    def test_if_user_tries_to_delete_task_board_that_does_not_exist_returns_404(
            self, user, api_client, valid_board_data):
        """
        Test that the user is authenticated, and if the user tries to delete task board that doesn't exist
        returns 404.
        :param user:
        :param api_client:
        :param valid_board_data:
        :return:
        """
        api_client.force_authenticate(user=user)
        api_client.post(f'/{user.username}/boards/', data=valid_board_data)

        response = api_client.delete(f'/{user.username}/boards/{'abcdefg'}/')

        assert response.status_code == status.HTTP_404_NOT_FOUND


