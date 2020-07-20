from django.db import models


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
