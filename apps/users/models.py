from django.contrib.auth.models import AbstractUser
from django.db import models
from django.utils.translation import gettext_lazy as _


class MyUser(AbstractUser):
    email = models.EmailField(_('email address'), unique=True)

    def is_owner(self, obj=None):
        return obj and obj.author.username == self.username

    class Meta:
        ordering = ('username',)
