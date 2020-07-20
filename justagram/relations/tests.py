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
        data = {
            'related_type': 'f'
        }

        url = f'/profile/{self.user.id}/follow'
        response = self.client.post(url, data=data)

        self.assertEqual(response.status_code, status.HTTP_201_CREATED)
        self.assertEqual(response.data['from_follow_user'], self.user.id)
        self.assertEqual(response.data['to_follow_user'], self.user.id)

    def test_update_follow(self):
        self.follow = Follow.objects.create(
            from_follow_user=self.user,
            to_follow_user=self.user,
            related_type='f'
        )
        self.client.force_authenticate(user=self.user)
        data = {
            'related_type': 'b'
        }

        url = f'/profile/{self.user.id}/follow/{self.follow.id}'
        response = self.client.patch(url, data=data)
        self.assertEqual(response.status_code, status.HTTP_200_OK)

    def test_delete_follow(self):
        self.client.force_authenticate(user=self.user)
        follow = Follow.objects.create(
            from_follow_user=self.user,
            to_follow_user=self.user,
            related_type='f'
        )

        url = f'/follow/{follow.id}'
        response = self.client.delete(url)

        self.assertEqual(response.status_code, status.HTTP_204_NO_CONTENT)
        self.assertFalse(Follow.objects.exists())
