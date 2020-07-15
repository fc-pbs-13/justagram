from rest_framework import status
from rest_framework.test import APITestCase

from comments.models import Comment
from posts.models import Post
from users.models import User


class CommentTestCase(APITestCase):
    def setUp(self) -> None:
        self.user = User.objects.create(
            email='user@user.com',
            name='user',
            username='user',
            password='user',
        )

        self.post = Post.objects.create(
            contents='test',
            owner=self.user,
        )

        self.comment = Comment.objects.create(
            comment='test',
            post=self.post,
            user=self.user,
        )

    def test_create_comment(self):
        data = {
            'comment': 'test',
        }
        self.client.force_authenticate(user=self.user)

        response = self.client.post(f'/user/{self.user.id}/post/{self.post.id}/comment', data=data)

        self.assertEqual(response.status_code, status.HTTP_201_CREATED)
        self.assertEqual(response.data['comment'], data['comment'])
        self.assertEqual(response.data['post'], self.post.id)
        self.assertEqual(response.data['user'], self.user.id)

    def test_create_reply(self):
        data = {
            'comment': 'test',
        }
        self.client.force_authenticate(user=self.user)
        response = self.client.post(f'/comment/{self.comment.id}/comment', data=data)
        print(response.data)
        self.assertEqual(response.status_code, status.HTTP_201_CREATED)
        self.assertEqual(response.data['comment'], data['comment'])
        self.assertEqual(response.data['parent'], self.comment.id)
        self.assertFalse(response.data['post'])

    def test_list_comment(self):
        self.client.force_authenticate(user=self.user)

        response = self.client.post()

    def test_update_comment(self):
        data = {
            'comment': 'update'
        }
        self.client.force_authenticate(user=self.user)

        response = self.client.patch(f'/comment/{self.comment.id}', data=data)

        self.assertEqual(response.status_code, status.HTTP_200_OK)
        self.assertEqual(response.data['comment'], data['comment'])

    def test_delete_comment(self):
        self.client.force_authenticate(user=self.user)
        response = self.client.delete(f'/comment/{self.comment.id}')

        self.assertEqual(response.status_code, status.HTTP_204_NO_CONTENT)
