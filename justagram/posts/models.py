from django.contrib.postgres.fields import ArrayField
from django.db import models


class Post(models.Model):
    owner = models.ForeignKey('users.UserProfile', on_delete=models.CASCADE())
    photo = ArrayField(models.ImageField())
    contents = models.TextField()
