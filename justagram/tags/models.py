from django.db import models


class Tag(models.Model):
    tag_name = models.CharField(max_length=50)
    count_tag = models.IntegerField(default=0)


class TagPost(models.Model):
    post = models.ForeignKey('posts.Post',
                             related_name='posts',
                             on_delete=models.CASCADE)
    tag = models.ForeignKey('tags.Tag',
                            related_name='tags',
                            on_delete=models.CASCADE)

    class Meta:
        unique_together = (
            ('post', 'tag')
        )
