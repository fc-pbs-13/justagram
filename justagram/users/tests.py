from rest_framework import status
from rest_framework.authtoken.models import Token
from rest_framework.test import APITestCase

from users.models import User


class UserCreateCase(APITestCase):
    """Create User Test Code"""

    def setUp(self) -> None:
        self.url = '/user'

        self.user = User.objects.create(
            email='user@user.com',
            name='user',
            username='user',
            password='user',
        )

    def test_success(self):
        """User 생성 성공"""
        data = {
            'email': 'test@test.com',
            'name': 'test',
            'username': 'test',
            'password': 'test',
        }
        response = self.client.post(self.url, data=data)

        self.assertEqual(response.status_code, status.HTTP_201_CREATED)
        self.assertEqual(response.data['email'], data['email'])
        self.assertEqual(response.data['name'], data['name'])
        self.assertEqual(response.data['username'], data['username'])

    def test_wrong_authenticate(self):
        """login 된 user 접근"""
        data = {
            'email': 'test@test.com',
            'name': 'test',
            'username': 'test',
            'password': 'test',
        }

        self.client.force_authenticate(user=self.user)
        response = self.client.post(self.url, data=data)

        self.assertEqual(response.status_code, status.HTTP_403_FORBIDDEN)

    def test_overlap_email(self):
        """email 중복"""
        data = {
            'email': 'user@user.com',
            'name': 'test',
            'username': 'test',
            'password': 'test',
        }
        response = self.client.post(self.url, data=data)

        self.assertEqual(response.status_code, status.HTTP_400_BAD_REQUEST)

    def test_overlap_username(self):
        """username 중복"""
        data = {
            'email': 'test@test.com',
            'name': 'test',
            'username': 'user',
            'password': 'test',
        }
        response = self.client.post(self.url, data=data)

        self.assertEqual(response.status_code, status.HTTP_400_BAD_REQUEST)

    def test_none_email(self):
        """email 미기입"""
        data = {
            'name': 'test',
            'username': 'test',
            'password': 'test',
        }
        response = self.client.post(self.url, data=data)

        self.assertEqual(response.status_code, status.HTTP_400_BAD_REQUEST)

    def test_none_name(self):
        """name 미기입"""
        data = {
            'email': 'test@test.com',
            'username': 'test',
            'password': 'test',
        }
        response = self.client.post(self.url, data=data)

        self.assertEqual(response.status_code, status.HTTP_400_BAD_REQUEST)

    def test_none_username(self):
        """username 미기입"""
        data = {
            'email': 'test@test.com',
            'name': 'test',
            'password': 'test',
        }
        response = self.client.post(self.url, data=data)

        self.assertEqual(response.status_code, status.HTTP_400_BAD_REQUEST)

    def test_none_password(self):
        """password 미기입"""
        data = {
            'email': 'test@test.com',
            'username': 'test',
            'name': 'test',
        }
        response = self.client.post(self.url, data=data)

        self.assertEqual(response.status_code, status.HTTP_400_BAD_REQUEST)

    def test_none_all(self):
        """미기입"""
        response = self.client.post(self.url)

        self.assertEqual(response.status_code, status.HTTP_400_BAD_REQUEST)


class UserDeleteCase(APITestCase):
    """Delete User Test Case"""

    def setUp(self) -> None:
        self.user = User.objects.create(
            email='user@user.com',
            name='user',
            username='user',
            password='user',
        )

        self.url = f'/user/{self.user.id}'

    def test_success(self):
        """User 삭제 성공"""
        self.client.force_authenticate(user=self.user)
        response = self.client.delete(self.url)

        self.assertEqual(response.status_code, status.HTTP_204_NO_CONTENT)
        self.assertFalse(User.objects.exists())

    def test_wrong_authenticate(self):
        """자신이 아닌 User 접근"""
        user = User.objects.create(
            email='test@test.com',
            name='test',
            username='test',
            password='test',
        )

        self.client.force_authenticate(user=user)

        response = self.client.delete(self.url)

        self.assertEqual(response.status_code, status.HTTP_403_FORBIDDEN)

    def test_anonymoususer(self):
        """AnonymousUser 접근"""
        response = self.client.delete(self.url)

        self.assertEqual(response.status_code, status.HTTP_401_UNAUTHORIZED)

    def test_wrong_url(self):
        """잘못된 url 접근"""
        self.client.force_authenticate(user=self.user)
        response = self.client.delete('user/wrong_url')

        self.assertEqual(response.status_code, status.HTTP_404_NOT_FOUND)


class UserRetrieveCase(APITestCase):
    """Retrieve User Test Case"""

    def setUp(self) -> None:
        self.user = User.objects.create(
            email='user@user.com',
            name='user',
            username='user',
            password='user',
        )

        self.url = f'/user/{self.user.id}'

    def test_success(self):
        """User Retrieve 접근 성공"""
        self.client.force_authenticate(user=self.user)
        response = self.client.get(self.url)

        self.assertEqual(status.HTTP_200_OK, response.status_code)
        self.assertEqual(response.data['email'], self.user.email)
        self.assertEqual(response.data['name'], self.user.name)
        self.assertEqual(response.data['username'], self.user.username)

    def test_wrong_authenticate(self):
        """자신이 아닌 User 접근"""
        user = User.objects.create(
            email='test@test.com',
            name='test',
            username='test',
            password='test',
        )

        self.client.force_authenticate(user=user)
        response = self.client.get(self.url)

        self.assertEqual(response.status_code, status.HTTP_403_FORBIDDEN)

    def test_anonymoususer(self):
        """AnonymousUser 접근"""
        response = self.client.get(self.url)

        self.assertEqual(response.status_code, status.HTTP_401_UNAUTHORIZED)

    def test_wrong_url(self):
        """틀린 id로 접근"""
        self.client.force_authenticate(user=self.user)
        response = self.client.get('user/wrong_url')

        self.assertEqual(response.status_code, status.HTTP_404_NOT_FOUND)


class ChangePasswordCase(APITestCase):
    """Change Password Test code"""

    def setUp(self) -> None:
        self.user = User.objects.create(
            email='user@user.com',
            name='user',
            username='user',
            password='user',
        )

        self.url = f'/user/{self.user.id}/change_password'

    def test_success(self):
        """password 변경 성"""
        data = {
            'password': 'user',
            'new_password1': 'test',
            'new_password2': 'test',
        }

        self.client.force_authenticate(user=self.user)
        response = self.client.put(self.url, data=data)

        self.assertEqual(response.status_code, status.HTTP_200_OK)
        self.user.check_password(data['new_password1'])

    def test_wrong_url(self):
        """잘못된 url 접근"""
        data = {
            'password': 'user',
            'new_password1': 'test',
            'new_password2': 'test',
        }

        self.client.force_authenticate(user=self.user)
        response = self.client.put('/user/wrong_url/change_password', data=data)

        self.assertEqual(response.status_code, status.HTTP_404_NOT_FOUND)

    def test_wrong_authenticate(self):
        """자신이 아닌 user 접근"""
        user = User.objects.create(
            email='test@test.com',
            name='test',
            username='test',
            password='test',
        )

        data = {
            'password': 'user',
            'new_password1': 'test',
            'new_password2': 'test',
        }

        self.client.force_authenticate(user=user)
        response = self.client.put(self.url, data=data)
        self.assertEqual(response.status_code, status.HTTP_403_FORBIDDEN)

    def test_anonymoususer(self):
        """AnonymousUser 접근"""
        data = {
            'password': 'user',
            'new_password1': 'test',
            'new_password2': 'test',
        }

        response = self.client.get(self.url, data=data)
        self.assertEqual(response.status_code, status.HTTP_405_METHOD_NOT_ALLOWED)

    def test_none_password(self):
        """password 미기입"""
        data = {
            'new_password1': 'test',
            'new_password2': 'test',
        }

        self.client.force_authenticate(user=self.user)
        response = self.client.put(self.url, data=data)
        self.assertEqual(response.status_code, status.HTTP_400_BAD_REQUEST)

    def test_none_new_password1(self):
        """password1 미기입"""
        data = {
            'password': 'user',
            'new_password2': 'test',
        }

        self.client.force_authenticate(user=self.user)
        response = self.client.put(self.url, data=data)
        self.assertEqual(response.status_code, status.HTTP_400_BAD_REQUEST)

    def test_none_new_password2(self):
        """password2 미기입"""
        data = {
            'password': 'user',
            'new_password1': 'test',
        }

        self.client.force_authenticate(user=self.user)
        response = self.client.put(self.url, data=data)
        self.assertEqual(response.status_code, status.HTTP_400_BAD_REQUEST)

    def test_none_all(self):
        """미기입"""
        self.client.force_authenticate(user=self.user)
        response = self.client.put(self.url)
        self.assertEqual(response.status_code, status.HTTP_400_BAD_REQUEST)


class LogInCase(APITestCase):
    def setUp(self) -> None:
        self.user = User.objects.create(
            email='user@user.com',
            name='user',
            username='user',
            password='user',
        )

        self.url = f'/user/login'

    def test_success(self):
        """login 성공"""
        data = {
            'email': 'user@user.com',
            'password': 'user'
        }

        response = self.client.post(self.url, data=data)

        self.assertEqual(response.status_code, status.HTTP_201_CREATED)
        self.assertTrue(Token.objects.exists())

    def test_authenticate(self):
        """인증된 user login 시도"""
        data = {
            'email': 'user@user.com',
            'password': 'user'
        }

        self.client.force_authenticate(user=self.user)
        response = self.client.post(self.url, data=data)

        self.assertEqual(response.status_code, status.HTTP_403_FORBIDDEN)

    def test_none_email(self):
        """email 미기입"""
        data = {
            'password': 'user'
        }
        response = self.client.post(self.url, data=data)

        self.assertEqual(response.status_code, status.HTTP_404_NOT_FOUND)

    def test_none_password(self):
        """password 미기입"""
        data = {
            'email': 'user@user.com'
        }
        response = self.client.post(self.url, data=data)

        self.assertEqual(response.status_code, status.HTTP_400_BAD_REQUEST)

    def test_none_all(self):
        """미기입"""
        response = self.client.post(self.url)

        self.assertEqual(response.status_code, status.HTTP_404_NOT_FOUND)


class LogOutCase(APITestCase):
    def setUp(self) -> None:
        self.user = User.objects.create(
            email='user@user.com',
            name='user',
            username='user',
            password='password'
        )

        self.token = Token.objects.create(
            user=self.user
        )

        self.url = '/user/logout'

    def test_success(self):
        self.client.force_authenticate(user=self.user)
        response = self.client.delete(self.url)

        self.assertEqual(response.status_code, status.HTTP_204_NO_CONTENT)
        self.assertFalse(Token.objects.all().exists())

    def test_anonymoususer(self):
        respone = self.client.delete(self.url)

        self.assertEqual(respone.status_code, status.HTTP_404_NOT_FOUND)
