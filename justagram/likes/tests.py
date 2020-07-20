from rest_framework import status
from rest_framework.test import APITestCase

from likes.models import PostLike
from posts.models import Post
from users.models import User


class PostViewSetTestCase(APITestCase):

    def setUp(self) -> None:
        self.user = User.objects.create(
            email='test@test.com',
            name='test',
            username='test',
            password='test',
        )

        self.post = Post.objects.create(
            contents='test',
            owner=self.user,
        )

    def test_create_like(self):
        self.client.force_authenticate(user=self.user)

        response = self.client.post(f'/post/{self.post.id}/post_like')
        self.assertEqual(response.status_code, status.HTTP_201_CREATED)

    def test_delete_like(self):
        self.client.force_authenticate(user=self.user)

        post_like = PostLike.objects.create(
            post_user=self.user,
            to_like_post=self.post
        )
        response = self.client.delete(f'/post_like/{post_like.id}')
        self.assertEqual(response.status_code, status.HTTP_204_NO_CONTENT)
        self.assertFalse(PostLike.objects.all().exists())
        self.fail()
