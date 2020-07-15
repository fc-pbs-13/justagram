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
        related_name='comments',
        null=True,
        blank=True
    )
    user = models.ForeignKey(
        'users.User',
        on_delete=models.CASCADE,
        related_name='comments'
    )
    comment = models.CharField(max_length=300)
