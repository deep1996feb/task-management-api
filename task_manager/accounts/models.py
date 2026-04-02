from django.db import models
from django.contrib.auth.models import AbstractUser
from .validators import custom_username_validator
# Create your models here.


class User(AbstractUser):
    username = models.CharField(max_length=150,unique=True,validators=[custom_username_validator])
    email = models.EmailField(unique=True)

    USERNAME_FIELD = 'email'
    REQUIRED_FIELDS = ['username']

    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)

    def __str__(self):
        return self.email