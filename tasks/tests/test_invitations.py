import pytest
from django.contrib.auth import get_user_model

from rest_framework import status

@pytest.mark.django_db
class TestPostInvitation:
    def test_post_invitation_if_user_is_anonymous_returns_401(self, api_client, user, valid_board_data, action_user):
        """
        Test if unauthorized user can invite another user to a task board. Expect 401 unauthorized status code.
        :param api_client:
        :param user:
        :param valid_board_data:
        :param action_user:
        """
        api_client.force_authenticate(user)
        api_client.post(f"/{user.username}/boards/", data=valid_board_data)
        api_client.logout()

        response = api_client.post(f"/boards/{valid_board_data['slug']}/invite/", data={
            "action": "invite",
            "username":action_user.username})

        assert response.status_code == status.HTTP_401_UNAUTHORIZED
        assert response.data


    def test_post_invitation_if_user_is_authenticated_returns_200(self, api_client, user, valid_board_data, action_user):
        """
        Test if authorized user can invite another user to their task board. Expect 200 ok status code.
        :param api_client:
        :param user:
        :param valid_board_data:
        :param action_user:
        :return:
        """
        api_client.force_authenticate(user)
        api_client.post(f"/{user.username}/boards/", data=valid_board_data)

        response = api_client.post(f"/boards/{valid_board_data['slug']}/invite/", data={
            "action": "invite",
            "username":action_user.username})

        assert response.status_code == status.HTTP_200_OK
        assert response.data


    def test_post_invitation_if_invited_user_does_not_exist_returns_404(self, api_client, user, valid_board_data,
                                                                        action_user):
        """
        Test if authorized user can invite another user to their task board, if other user doesn't exist.
        Expect 404 not found status code.
        :param api_client:
        :param user:
        :param valid_board_data:
        :param action_user:
        :return:
        """
        api_client.force_authenticate(user)
        api_client.post(f"/{user.username}/boards/", data=valid_board_data)

        response = api_client.post(f"/boards/{valid_board_data['slug']}/invite/", data={
            "action": "invite",
            "username":"does-not-exist"})

        assert response.status_code == status.HTTP_404_NOT_FOUND
        assert response.data

    def test_post_invitation_if_board_does_not_exist_returns_404(self, api_client, user, valid_board_data, action_user):
        """
        Test if authorized user can invite another user to a task board, if task board doesn't exist.
        Expect 404 not found status code.
        :param api_client:
        :param user:
        :param valid_board_data:
        :param action_user:
        :return:
        """
        api_client.force_authenticate(user)

        response = api_client.post(f"/boards/'imgoingtotrythisslug'/invite/", data={
            "action": "invite",
            "username": action_user.username})

        assert response.status_code == status.HTTP_404_NOT_FOUND
        assert response.data

    def test_post_invitation_if_no_username_returns_400(self, api_client, user, valid_board_data, action_user):
        """
        Test if user can invite another user to their task board, if user leaves username blank.
        Expect 400 bad request status code.
        :param api_client:
        :param user:
        :param valid_board_data:
        :param action_user:
        :return:
        """
        api_client.force_authenticate(user)
        api_client.post(f"/{user.username}/boards/", data=valid_board_data)

        response = api_client.post(f"/boards/{valid_board_data['slug']}/invite/", data={
            "action": "invite",

        })

        assert response.status_code == status.HTTP_400_BAD_REQUEST
        assert response.data

    def test_post_invitation_if_user_already_invited_returns_400(self, api_client, user, valid_board_data, action_user):
        """
        Test if user can invite another user to their task board, if user is already invited to the taskboard.
        Expect 400 bad request status code.
        :param api_client:
        :param user:
        :param valid_board_data:
        :param action_user:
        :return:
        """
        api_client.force_authenticate(user)
        api_client.post(f"/{user.username}/boards/", data=valid_board_data)
        api_client.post(f"/boards/{valid_board_data['slug']}/invite/", data={
            "action": "invite",
            "username": action_user.username
        })

        response = api_client.post(f"/boards/{valid_board_data['slug']}/invite/", data={
            "username": action_user.username
        })

        assert response.status_code == status.HTTP_400_BAD_REQUEST
        assert response.data

    def test_post_invitation_user_cannot_invite_self_returns_400(self,
                                                                 api_client, user, valid_board_data, action_user):
        """
        Test user cannot invite themselves to their task board. Expect 400 bad request status code.
        :param api_client:
        :param user:
        :param valid_board_data:
        :param action_user:
        :return:
        """
        api_client.force_authenticate(user)
        api_client.post(f"/{user.username}/boards/", data=valid_board_data)

        response = api_client.post(f"/boards/{valid_board_data['slug']}/invite/", data={
            "action": "invite",
            "username": user.username
        })
        assert response.status_code == status.HTTP_400_BAD_REQUEST
        assert response.data

    def test_post_invitation_if_action_not_provided(self, api_client, user, valid_board_data, action_user):
        """
        Test if user cannot invite another user to their task board if action not provided.
         Expect 400 bad request status code.
        :param api_client:
        :param user:
        :param valid_board_data:
        :param action_user:
        :return:
        """
        api_client.force_authenticate(user)
        api_client.post(f"/{user.username}/boards/", data=valid_board_data)

        response = api_client.post(f"/boards/{valid_board_data["slug"]}/invite/", data={
            "username": action_user.username
        })
        assert response.status_code == status.HTTP_400_BAD_REQUEST
        assert response.data

@pytest.mark.django_db
class TestPostInvitationRemove:
    def test_post_remove_if_user_is_anonymous_returns_401(self, api_client, user, valid_board_data, action_user):
        """
        Test if unauthorized user cannot remove another user from a task board. Expect 401 unauthorized status code.
        :return:
        """
        api_client.force_authenticate(user)
        api_client.post(f"/{user.username}/boards/", data=valid_board_data)
        api_client.logout()
        api_client.post(f"/boards/{valid_board_data['slug']}/invite/", data={
            "action": "invite",
            "username":action_user.username})

        response = api_client.post(f"/boards/{valid_board_data["slug"]}/invite/", data={
            "action": "remove",
            "username":action_user.username})

        assert response.status_code == status.HTTP_401_UNAUTHORIZED
        assert response.data

    def test_post_remove_if_user_is_authorized_returns_200(self, api_client, user, valid_board_data, action_user):
        """
        Test if user can remove another user from their task board. Expect 200 status code.
        :param api_client:
        :param user:
        :param valid_board_data:
        :param action_user:
        :return:
        """
        api_client.force_authenticate(user)
        api_client.post(f"/{user.username}/boards/", data=valid_board_data)
        api_client.post(f"/boards/{valid_board_data["slug"]}/invite/", data={
            "action": "invite",
            "username":action_user.username})

        response = api_client.post(f"/boards/{valid_board_data["slug"]}/invite/", data={
            "action": "remove",
            "username": action_user.username})

        assert response.status_code == status.HTTP_200_OK
        assert response.data

    def test_post_remove_if_user_does_not_exist(self, api_client, user, valid_board_data, action_user):
        """
        Test if user cannot remove another user from their task board if the other user does not exist.
         Expect 404 status code.
        :param api_client:
        :param user:
        :param valid_board_data:
        :param action_user:
        :return:
        """
        api_client.force_authenticate(user)
        api_client.post(f"/{user.username}/boards/", data=valid_board_data)
        api_client.post(f"/boards/{valid_board_data["slug"]}/invite/", data={
            "action": "invite",
            "username": action_user.username})

        response = api_client.post(f"/boards/{valid_board_data["slug"]}/invite/", data={
            "action": "remove",
            "username": "doesnotexist"})

        assert response.status_code == status.HTTP_404_NOT_FOUND
        assert response.data

    def test_post_remove_if_task_board_does_not_exist(self, api_client, user, valid_board_data, action_user):
        """
        Test if user cannot remove another user from their task board when task board doesn't exist.
         Expect 404 status code.
        :param api_client:
        :param user:
        :param valid_board_data:
        :param action_user:
        :return:
        """
        api_client.force_authenticate(user)


        response = api_client.post(f"/boards/'abc'/invite/", data={
            "action": "remove",
            "username": "doesnotexist"})

        assert response.status_code == status.HTTP_404_NOT_FOUND
        assert response.data

    def test_post_remove_if_username_not_provided(self, api_client, user, valid_board_data, action_user):
        """
        Test if user cannot remove another user from their task board if the user doesn't provide username.
         Expect 400 status code.
        :param api_client:
        :param user:
        :param valid_board_data:
        :param action_user:
        :return:
        """
        api_client.force_authenticate(user)
        api_client.post(f"/{user.username}/boards/", data=valid_board_data)
        api_client.post(f"/boards/{valid_board_data["slug"]}/invite/", data={
            "action": "invite",
            "username": action_user.username})

        response = api_client.post(f"/boards/{valid_board_data["slug"]}/invite/", data={
            "action": "remove"})

        assert response.status_code == status.HTTP_400_BAD_REQUEST
        assert response.data

    def test_post_remove_if_action_not_provided(self, api_client, user, valid_board_data, action_user):
        """
        Test if user cannot remove another user from their task board if the user doesn't provide action.
        Expect 400 status code.
        :param api_client:
        :param user:
        :param valid_board_data:
        :param action_user:
        :return:
        """
        api_client.force_authenticate(user)
        api_client.post(f"/{user.username}/boards/", data=valid_board_data)
        api_client.post(f"/boards/{valid_board_data["slug"]}/invite/", data={
            "action": "invite",
            "username": action_user.username})

        response = api_client.post(f"/boards/{valid_board_data["slug"]}/invite/", data={
            "username": action_user.username})

        assert response.status_code == status.HTTP_400_BAD_REQUEST
        assert response.data

    def test_post_remove_if_user_is_not_guest(self, api_client, user, valid_board_data, action_user):
        """
        Test if user cannot remove another user from their task board if the user isn't a guest on their taskboard.
        Expect 400 status code.
        :param api_client:
        :param user:
        :param valid_board_data:
        :param action_user:
        :return:
        """
        User = get_user_model()
        valid_user = User.objects.create_user(username="MrPoopyButhole", password="Meeseeks")
        api_client.force_authenticate(user)
        api_client.post(f"/{user.username}/boards/", data=valid_board_data)
        api_client.post(f"/boards/{valid_board_data["slug"]}/invite/", data={
            "action": "invite",
            "username": action_user.username})


        response = api_client.post(f"/boards/{valid_board_data["slug"]}/invite/", data={
            "action": "remove",
            "username": valid_user.username,
        })

        assert response.status_code == status.HTTP_400_BAD_REQUEST
        assert response.data

    def test_post_remove_cannot_remove_self(self, api_client, user, valid_board_data, action_user):
        """
        Test if user cannot remove themselves from their task board.
        :param api_client:
        :param user:
        :param valid_board_data:
        :param action_user:
        :return:
        """
        api_client.force_authenticate(user)
        api_client.post(f"/{user.username}/boards/", data=valid_board_data)
        api_client.post(f"/boards/{valid_board_data["slug"]}/invite/", data={
            "action": "invite",
            "username": action_user.username})

        response = api_client.post(f"/boards/{valid_board_data["slug"]}/invite/", data={
            "action": "remove",
            "username": user.username,
        })

        assert response.status_code == status.HTTP_400_BAD_REQUEST
        assert response.data






