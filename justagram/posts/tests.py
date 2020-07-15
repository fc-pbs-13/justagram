import io

from PIL import Image
from rest_framework import status
from rest_framework.test import APITestCase

from posts.models import Post
from users.models import User


class PostViewSetTestCase(APITestCase):
    def generate_photo_file(self):
        file = io.BytesIO()
        image = Image.new('RGBA', size=(1, 1), color=(0, 0, 0))
        image.save(file, 'png')
        file.name = 'test.png'
        file.seek(0)
        return file

    def setUp(self) -> None:
        self.user = User.objects.create(
            email='user@user.com',
            name='user',
            username='user',
            password='user',
        )

        self.multiple_data = {
            'input_photo': [self.generate_photo_file(), self.generate_photo_file()],
            'contents': 'hello'
        }

        self.post = Post.objects.create(
            contents='test',
            owner=self.user,
        )

    def test_create_post(self):
        self.client.force_authenticate(user=self.user)

        response = self.client.post(f'/post', data=self.multiple_data)
        self.assertEqual(response.status_code, status.HTTP_201_CREATED)
        self.assertEqual(response.data['contents'], self.multiple_data['contents'])
        self.assertEqual(len(response.data['photo']), len(self.multiple_data['input_photo']))

    def test_list_post(self):
        self.client.force_authenticate(user=self.user)

        response = self.client.get('/post')
        self.assertEqual(response.status_code, status.HTTP_200_OK)

    def test_update_post(self):
        data = {'contents': 'good', }
        self.client.force_authenticate(user=self.user)

        response = self.client.patch(f'/post/{self.post.id}', data=data)

        self.assertEqual(response.status_code, status.HTTP_200_OK)
        self.assertEqual(response.data['contents'], data['contents'])

    def test_delete_post(self):
        self.client.force_authenticate(user=self.user)
        response = self.client.delete(f'/post/{self.post.id}')

        self.assertEqual(response.status_code, status.HTTP_204_NO_CONTENT)
        self.assertFalse(Post.objects.exists())
