import io

from PIL import Image
from rest_framework import status
from rest_framework.test import APITestCase

from stories.models import Story
from users.models import User


class StoryTestCase(APITestCase):

    def setUp(self) -> None:
        self.user = User.objects.create(
            email='user@user.com',
            name='user',
            username='username',
            password='username',
        )

        file = io.BytesIO()
        image = Image.new('RGBA', size=(1, 1), color=(0, 0, 0))
        image.save(file, 'png')
        file.name = 'test.png'
        file.seek(0)

        self.img = file

    def test_create_story(self):
        self.client.force_authenticate(user=self.user)
        data = {
            'image': self.img
        }
        response = self.client.post('/story', data=data)

        self.assertEqual(response.status_code, status.HTTP_201_CREATED)

    def test_list_story(self):
        story = []
        for i in range(3):
            instance = Story.objects.create(
                user=self.user,
            )
            story.append(instance)

        self.client.force_authenticate(user=self.user)
        response = self.client.get('/story')

        self.assertEqual(response.status_code, status.HTTP_200_OK)

        list = Story.objects.filter(user=self.user)

        self.assertEqual(len(response.data), len(list))

    def test_delete_story(self):
        story = Story.objects.create(
            user=self.user
        )

        self.client.force_authenticate(user=self.user)
        response = self.client.delete(f'/story/{story.id}')

        self.assertEqual(response.status_code, status.HTTP_204_NO_CONTENT)
        self.assertFalse(Story.objects.filter(id=story.id).exists())
