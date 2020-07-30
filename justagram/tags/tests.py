import io

from PIL import Image
from rest_framework import status
from rest_framework.test import APITestCase

from posts.models import Post
from tags.models import TagPost, Tag
from users.models import User


class TagTestCase(APITestCase):
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
        )

        self.data = {
            'contents': 'test',
            'input_photo': [self.generate_photo_file(), self.generate_photo_file()],
            'tag': ['강', '강아', '강아지', '강아징']
        }

    def test_create_tag(self):
        self.client.force_authenticate(user=self.user)
        response = self.client.post('/post', data=self.data)

        self.assertEqual(response.status_code, status.HTTP_201_CREATED)
        self.assertEqual(len(self.data['tag']), Tag.objects.all().count())
        self.fail()
