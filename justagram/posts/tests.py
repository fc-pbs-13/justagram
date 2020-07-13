from rest_framework import status
from rest_framework.test import APITestCase

from posts.models import Post
from users.models import User


class PostViewSetTestCase(APITestCase):
    def setUp(self) -> None:
        self.user = User.objects.create(
            email='user@user.com',
            name='user',
            username='user',
            password='user',
        )

        self.post = Post.objects.create(
            contents='test',
            owner=self.user.profile
        )

    def test_create_post(self):
        data = {'contents': 'test',
                'image': 'test',
                }
        self.client.force_authenticate(user=self.user)

        response = self.client.post(f'/api/post', data=data)
        print(response.data)
        self.assertEqual(response.status_code, status.HTTP_201_CREATED)
        self.assertEqual(response.data['contents'], data['contents'])
        self.fail()

    def test_update_post(self):
        data = {'contents': 'good', }
        self.client.force_authenticate(user=self.user)

        response = self.client.put(f'/api/post/{self.post.id}', data=data)

        self.assertEqual(response.status_code, status.HTTP_200_OK)
        self.assertEqual(response.data['contents'], data['contents'])
        self.fail()

    def test_delete_post(self):
        self.client.force_authenticate(user=self.user)
        response = self.client.delete(f'/api/post/{self.post.id}')

        self.assertEqual(response.status_code, status.HTTP_204_NO_CONTENT)
        self.assertFalse(Post.objects.exists())
        self.fail()
