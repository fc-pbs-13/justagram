from django.db import models


class Post(models.Model):
    owner = models.ForeignKey('users.User',
                              related_name='post',
                              on_delete=models.CASCADE,
                              )
    contents = models.TextField()


class Photo(models.Model):
    post = models.ForeignKey('posts.Post',
                             related_name='photo',
                             on_delete=models.CASCADE,
                             )
    post_image = models.ImageField(upload_to='post_photo')
