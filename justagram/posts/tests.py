from rest_framework import status
from rest_framework.test import APITestCase

from users.models import User, UserProfile


class PostViewSetTestCase(APITestCase):
    def setUp(self) -> None:
        self.user = User.objects.create(
            email='user@user.com',
            name='user',
            username='user',
            password='user',
        )
        self.profile = UserProfile.objects.all()
        print(self.profile)

    def test_create(self):
        data = {
            'contents': 'test',
        }
        response = self.client.post(f'/api/post', data=data)
        self.assertEqual(response.status_code, status.HTTP_201_CREATED)
        self.fail()
