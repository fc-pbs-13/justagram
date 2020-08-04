from django.contrib.auth.models import (
    AbstractUser, UserManager
)
from django.db import models
from django_lifecycle import LifecycleModel, hook, AFTER_CREATE, AFTER_SAVE, BEFORE_CREATE


class MyUserManager(UserManager):
    def _create_user(self, email, username, name, password, **extra_fields):
        if not username:
            raise ValueError('The given email must be set')
        email = self.normalize_email(email)
        username = self.model.normalize_username(username)
        name = name
        user = self.model(username=username, email=email, name=name, password=password, **extra_fields)
        user.save()
        return user

    def create_user(self, email, username, name, password=None, **extra_fields):
        extra_fields.setdefault('is_staff', False)
        extra_fields.setdefault('is_superuser', False)
        return self._create_user(email, username, name, password, **extra_fields)

    def create_superuser(self, email, username, name, password=None, **extra_fields):
        extra_fields.setdefault('is_staff', True)
        extra_fields.setdefault('is_superuser', True)

        if extra_fields.get('is_staff') is not True:
            raise ValueError('Superuser must have is_staff=True.')
        if extra_fields.get('is_superuser') is not True:
            raise ValueError('Superuser must have is_superuser=True.')

        return self._create_user(email, username, name, password, **extra_fields)


class User(AbstractUser, LifecycleModel):
    email = models.EmailField(
        verbose_name='이메일',
        max_length=255,
        unique=True,
    )
    name = models.CharField(
        verbose_name='성명',
        max_length=200,
    )

    objects = MyUserManager()

    USERNAME_FIELD = 'email'
    REQUIRED_FIELDS = ['name', 'username']

    def __str__(self):
        return self.email

    # def save(self, *args, **kwargs):
    #     self.set_password(self.password)
    #
    #     if not self.pk:
    #         super().save(*args, **kwargs)
    #         UserProfile.objects.create(
    #             user=self
    #         )
    #     else:
    #         super().save(*args, **kwargs)

    @hook(BEFORE_CREATE)
    def hash_password(self):
        print(self)
        self.set_password(self.password)

    @hook(AFTER_CREATE)
    def create_profile(self):
        UserProfile.objects.create(
            user=self
        )


class UserProfile(LifecycleModel):
    user = models.OneToOneField(
        'users.User',
        related_name='profile',
        on_delete=models.CASCADE,
    )
    web_site = models.CharField(
        verbose_name='웹사이트',
        max_length=50,
        null=True,
    )
    introduction = models.TextField(
        verbose_name='소개글',
        null=True,
    )
    # 내가 팔로우 한 사람
    following_count = models.IntegerField(
        default=0
    )
    # 나를 팔로우 한 사람
    follower_count = models.IntegerField(
        default=0
    )
    post_count = models.IntegerField(
        default=0
    )

    # @hook(AFTER_SAVE, when='user.name')
    # def create_profile(self):
    #     print('1')
    #     self.set_password(self.password)
    #
    #     if not self.pk:
    #         UserProfile.objects.create(
    #             user=self
    #         )
