from django.db import models
from django.db.models import F

from users.models import UserProfile


class Post(models.Model):
    owner = models.ForeignKey('users.User',
                              related_name='post',
                              on_delete=models.CASCADE,
                              )
    contents = models.TextField()
    like_count = models.IntegerField(default=0)

    def save(self, *args, **kwargs):
        super().save(*args, **kwargs)

        post = UserProfile.objects.filter(id=self.owner_id)
        post.update(post_count=F('post_count')+1)


class Photo(models.Model):
    post = models.ForeignKey('posts.Post',
                             related_name='photo',
                             on_delete=models.CASCADE,
                             )
    post_image = models.ImageField(upload_to='post_photo')
