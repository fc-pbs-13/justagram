from rest_framework import status
from rest_framework.test import APITestCase

from users.models import UserProfile, User


class UserTestCase(APITestCase):
    def setUp(self) -> None:
        self.data = {
            'email': 'test@test.com',
            'name': 'test',
            'nickname': 'test',
            'password': 'test',
        }
        self.user = User.objects.create(
            email='user@user.com',
            name='user',
            nickname='user',
            password='user',
        )

    def test_create_user(self):
        # Create user test code
        response = self.client.post('/api/signup', data=self.data)
        self.assertEqual(response.status_code, status.HTTP_201_CREATED)
        self.assertEqual(response.data['email'], self.data['email'])
        self.assertEqual(response.data['name'], self.data['name'])
        self.assertEqual(response.data['nickname'], self.data['nickname'])

        # Create userprofile test code
        profile = UserProfile.objects.get(user__email=response.data['email'])
        self.assertEqual(response.data['email'], profile.user.email)
        self.assertEqual(response.data['name'], profile.user.name)
        self.assertEqual(response.data['nickname'], profile.user.nickname)

    def test_delete_user(self):
        response = self.client.delete('/api/signup/1')
        self.assertEqual(status.HTTP_204_NO_CONTENT, response.status_code)
        self.assertFalse(User.objects.count())
        self.assertFalse(UserProfile.objects.count())

    def test_user_signup(self):
        self.fail()

    def test_user_signout(self):
        self.fail()
