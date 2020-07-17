from rest_framework import status
from rest_framework.test import APITestCase

from relations.models import Follow
from users.models import User


class FollowTestCase(APITestCase):
    def setUp(self) -> None:
        self.user = User.objects.create(
            email='user@user.com',
            name='user',
            username='user',
            password='user',
        )

    def test_create_follow(self):
        self.client.force_authenticate(user=self.user)

        url = f'/profile/{self.user.id}/follow'
        response = self.client.post(url)
        response2 = self.client.post(url)
        print(response2)

        self.assertEqual(response.status_code, status.HTTP_201_CREATED)
        self.assertEqual(response.data['from_follow_user'], self.user.id)
        self.assertEqual(response.data['to_follow_user'], self.user.id)

    def test_delete_follow(self):
        self.client.force_authenticate(user=self.user)
        follow = Follow.objects.create(
            from_follow_user=self.user,
            to_follow_user=self.user
        )

        url = f'/follow/{follow.id}'
        response = self.client.delete(url)

        self.assertEqual(response.status_code, status.HTTP_204_NO_CONTENT)
        self.assertFalse(Follow.objects.exists())
