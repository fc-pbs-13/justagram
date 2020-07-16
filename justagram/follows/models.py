from django.db import models
from django.db.models import F

from users.models import UserProfile


class Follow(models.Model):
    CHOICE_RELATIONS_TYPE = (
        ('f', 'follow'),
        ('b', 'block'),
    )
    related_type = models.CharField(
        choices=CHOICE_RELATIONS_TYPE,
        max_length=10,
    )
    from_follow_user = models.ForeignKey(
        'users.User',
        on_delete=models.CASCADE,
        related_name='from_follow_user'
    )
    to_follow_user = models.ForeignKey(
        'users.User',
        on_delete=models.CASCADE,
        related_name='to_follow_user'
    )

    class Meta:
        unique_together = (
            ('from_follow_user', 'to_follow_user'),
        )

    def save(self, *args, **kwargs):
        from_user = UserProfile.objects.filter(id=self.from_follow_user_id)
        to_user = UserProfile.objects.filter(id=self.to_follow_user_id)
        super().save(*args, **kwargs)
        if self.related_type == 'f':
            from_user.update(following_count=F('following_count') + 1)
            to_user.update(follower_count=F('follower_count') + 1)

    def delete(self, using=None, keep_parents=False):
        from_user = UserProfile.objects.filter(id=self.from_follow_user_id)
        to_user = UserProfile.objects.filter(id=self.to_follow_user_id)
        super().delete()
        if self.related_type == 'f':
            from_user.update(following_count=F('following_count') - 1)
            to_user.update(follower_count=F('follower_count') - 1)
