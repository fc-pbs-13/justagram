from django.db import models


class PostLike(models.Model):
    from_like_post = models.ForeignKey('users.User',
                                       null=True,
                                       on_delete=models.CASCADE,
                                       related_name='from_like_post'
                                       )
    to_like_post = models.ForeignKey('posts.Post',
                                     null=True,
                                     on_delete=models.CASCADE,
                                     related_name='to_like_post'
                                     )

    class Meta:
        unique_together = (
            ('from_like_post', 'to_like_post')
        )


class CommentLike(models.Model):
    from_like_comment = models.ForeignKey('users.User',
                                          null=True,
                                          on_delete=models.CASCADE,
                                          related_name='from_like_comment'
                                          )
    to_like_comment = models.ForeignKey('comments.Comment',
                                        null=True,
                                        on_delete=models.CASCADE,
                                        related_name='to_like_comment'
                                        )

    class Meta:
        unique_together = (
            ('from_like_comment', 'to_like_comment')
        )
