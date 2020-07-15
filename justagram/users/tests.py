from rest_framework import status
from rest_framework.authtoken.models import Token
from rest_framework.test import APITestCase

from users.models import UserProfile, User


class UserTestCase(APITestCase):
    def setUp(self) -> None:
        self.data = {
            'email': 'test@test.com',
            'name': 'test',
            'username': 'test',
            'password': 'test',
        }
        self.user = User.objects.create(
            email='user@user.com',
            name='user',
            username='user',
            password='user',
        )

    def test_user_create(self):
        # Create user test code
        response = self.client.post('/user', data=self.data)

        self.assertEqual(response.status_code, status.HTTP_201_CREATED)
        self.assertEqual(response.data['email'], self.data['email'])
        self.assertEqual(response.data['name'], self.data['name'])
        self.assertEqual(response.data['username'], self.data['username'])

        # Create userprofile test code
        profile = UserProfile.objects.get(user__email=response.data['email'])

        self.assertEqual(response.data['email'], profile.user.email)
        self.assertEqual(response.data['name'], profile.user.name)
        self.assertEqual(response.data['username'], profile.user.username)

    def test_user_delete(self):
        self.client.force_authenticate(user=self.user)
        response = self.client.delete(f'/user/{self.user.pk}')

        self.assertEqual(status.HTTP_204_NO_CONTENT, response.status_code)
        self.assertFalse(User.objects.count())
        self.assertFalse(UserProfile.objects.count())

    def test_user_retrieve(self):
        self.client.force_authenticate(user=self.user)
        response = self.client.get(f'/user/{self.user.pk}')
        self.assertEqual(status.HTTP_200_OK, response.status_code)

    def test_user_update_password(self):
        data = {
            'password': 'user',
            'new_password1': '1',
            'new_password2': '1',

        }

        self.client.force_authenticate(user=self.user)
        response = self.client.put(f'/user/{self.user.pk}/change_password', data=data)

        self.assertEqual(status.HTTP_200_OK, response.status_code)

        response = self.client.post('/user/login', data={'email': 'user@user.com', 'password': '1'})
        self.assertEqual(response.status_code, status.HTTP_201_CREATED)

    def test_user_login(self):
        response = self.client.post('/user/login',
                                    data={'email': 'user@user.com', 'password': 'user'})

        self.assertEqual(status.HTTP_201_CREATED, response.status_code)
        self.assertTrue(Token.objects.exists())

    def test_user_logout(self):
        Token.objects.create(user=self.user)

        self.client.force_authenticate(user=self.user)
        response = self.client.delete('/user/logout')

        self.assertEqual(status.HTTP_204_NO_CONTENT, response.status_code)
        self.assertFalse(Token.objects.exists())

    def test_profile_update(self):
        self.client.force_authenticate(user=self.user)

        data = {
            'name': '1',
            'username': '1',
            'web_site': '1',
            'introduction': '1',
        }
        response = self.client.put(f'/profile/{self.user.pk}',
                                   data=data)

        self.assertEqual(response.status_code, status.HTTP_200_OK)

        self.assertEqual(response.data['name'], data['name'])
        self.assertEqual(response.data['username'], data['username'])
        self.assertEqual(response.data['web_site'], data['web_site'])
        self.assertEqual(response.data['introduction'], data['introduction'])

