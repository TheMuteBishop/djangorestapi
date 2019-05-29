from django.db import models
from django.contrib.auth.models import AbstractBaseUser, BaseUserManager, \
    PermissionsMixin


class UserManager(BaseUserManager):

    def create_user(self, email, password=None, **other_fileds):
        """ create new user with email """

        # normalize email
        if not email:
            raise ValueError('Email field is required')
        email = self.normalize_email(email)
        user = self.model(email=email, **other_fileds)
        user.set_password(password)
        user.save(using=self._db)
        return user

    def create_superuser(self, email, password):
        user = self.create_user(email, password)
        user.is_staff = True
        user.is_superuser = True
        user.save(using=self._db)
        return user


class User(AbstractBaseUser, PermissionsMixin):
    """ custom user  model to use email """

    email       = models.EmailField(max_length=225, unique=True)
    name        = models.CharField(max_length=225)
    is_active   = models.BooleanField(default=True)
    is_staff   = models.BooleanField(default=False)

    objects = UserManager()

    USERNAME_FIELD = 'email'
