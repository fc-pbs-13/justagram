from django.db import models
from django.contrib.auth.models import (
    BaseUserManager, AbstractBaseUser
)


class MyUserManager(BaseUserManager):
    def create_user(self, email, name, nickname, password=None):
        """
        Creates and saves a User with the given email, date of
        birth and password.
        """
        if not email:
            raise ValueError('Users must have an email address')

        user = self.model(
            email=self.normalize_email(email),
            name=name,
            nickname=nickname,
            password=password
        )

        # user.set_password(password)
        user.save()
        return user

    def create_superuser(self, email, name, nickname, password=None):
        """
        Creates and saves a superuser with the given email, date of
        birth and password.
        """
        user = self.create_user(
            email,
            name=name,
            nickname=nickname,
            password=password,
        )
        user.is_admin = True
        user.save(using=self._db)
        return user


class User(AbstractBaseUser):
    email = models.EmailField(
        verbose_name='이메일',
        max_length=255,
        unique=True,
    )
    name = models.CharField(
        verbose_name='성명',
        max_length=200,
    )
    nickname = models.CharField(
        verbose_name='사용자 이름',
        max_length=50,
        unique=True,
    )
    is_active = models.BooleanField(default=True)
    is_admin = models.BooleanField(default=False)

    objects = MyUserManager()

    USERNAME_FIELD = 'email'
    REQUIRED_FIELDS = ['name', 'nickname']

    def __str__(self):
        return self.email

    def has_perm(self, perm, obj=None):
        "Does the user have a specific permission?"
        # Simplest possible answer: Yes, always
        return True

    def has_module_perms(self, app_label):
        "Does the user have permissions to view the app `app_label`?"
        # Simplest possible answer: Yes, always
        return True

    @property
    def is_staff(self):
        "Is the user a member of staff?"
        # Simplest possible answer: All admins are staff
        return self.is_admin

    def save(self, *args, **kwargs):
        self.set_password(self.password)
        super().save(*args, **kwargs)

        if not UserProfile.objects.filter(pk=self.pk):
            UserProfile.objects.create(
                user=self
            )


class UserProfile(models.Model):
    user = models.OneToOneField(
        'users.User',
        related_name='user',
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
