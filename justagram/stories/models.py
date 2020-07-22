from django.db import models


class Story(models.Model):
    user = models.ForeignKey('users.User',
                             related_name='stories',
                             on_delete=models.CASCADE,
                             )
    time = models.DateTimeField(auto_now_add=True)
    image = models.ImageField(upload_to='story_image',
                              null=True)


class CheckShow(models.Model):
    show_story = models.ForeignKey('stories.Story',
                                   related_name='show_stories',
                                   on_delete=models.CASCADE
                                   )
    show_user = models.ForeignKey('users.User',
                                  related_name='show_users',
                                  on_delete=models.CASCADE
                                  )

    class Meta:
        unique_together = (
            ('show_story', 'show_user'),
        )
