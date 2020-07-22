from django.db import models
from django.db.models import F

from comments.models import Comment
from posts.models import Post


class PostLike(models.Model):
    post_user = models.ForeignKey('users.User',
                                  null=True,
                                  on_delete=models.CASCADE,
                                  related_name='post_user'
                                  )
    to_like_post = models.ForeignKey('posts.Post',
                                     null=True,
                                     on_delete=models.CASCADE,
                                     related_name='to_like_post'
                                     )

    class Meta:
        unique_together = (
            ('post_user', 'to_like_post')
        )

    def save(self, *args, **kwargs):
        super().save(*args, **kwargs)

        post = Post.objects.filter(id=self.post_user_id)
        post.update(like_count=F('like_count') + 1)


class CommentLike(models.Model):
    comment_user = models.ForeignKey('users.User',
                                     null=True,
                                     on_delete=models.CASCADE,
                                     related_name='comment_user'
                                     )
    to_like_comment = models.ForeignKey('comments.Comment',
                                        null=True,
                                        on_delete=models.CASCADE,
                                        related_name='to_like_comment'
                                        )

    class Meta:
        unique_together = (
            ('comment_user', 'to_like_comment')
        )

    def save(self, *args, **kwargs):
        super().save(*args, **kwargs)

        comment = Comment.objects.filter(id=self.comment_user_id)
        comment.update(like_count=F('like_count') + 1)
