from django.core.cache import cache
from django.db import models
from mptt.fields import TreeForeignKey
from mptt.models import MPTTModel


class Comment(MPTTModel):
    parent = TreeForeignKey(
        'self',
        on_delete=models.CASCADE,
        null=True,
        blank=True,
        related_name='children'
    )
    post = models.ForeignKey(
        'posts.Post',
        on_delete=models.CASCADE,
        related_name='post_comments',
        null=True,
        blank=True
    )
    user = models.ForeignKey(
        'users.User',
        on_delete=models.CASCADE,
        related_name='comments'
    )
    comment = models.CharField(max_length=300)
    like_count = models.IntegerField(default=0)

    # def save(self, *args, **kwargs):
    #     comment_id = self.id
    #     super().save(*args, **kwargs)
    #     if comment_id:
    #         cache.delete(f'comment_qs_{comment_id}')
    #
    # def delete(self, *args, **kwargs):
    #     comment_id = self.id
    #     super().delete(*args, **kwargs)
    #     cache.delete(f'comment_qs_{comment_id}')
