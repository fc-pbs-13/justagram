import io

from PIL import Image
from rest_framework.test import APITestCase

from posts.models import Post
from tags.models import TagPost
from users.models import User


class TagTestCase(APITestCase):
    def setUp(self) -> None:
        file = io.BytesIO()
        image = Image.new('RGBA', size=(1, 1), color=(0, 0, 0))
        image.save(file, 'png')
        file.name = 'test.png'
        file.seek(0)

        self.img = file

        self.data = {
            'contents': 'test',
            'input_photo': [self.img, self.img],
            'tag': ['멍', '냥']
        }

        self.user = User.objects.create(
            email='user@user.com',
            name='user',
            usernae='user',

        )

    def test_tag_relation(self):


        response = self.client.post('/post', data=self.data)

        self.assertEqual()
