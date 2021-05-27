from django.contrib.auth.models import AbstractUser
from django.db import models
from django.utils.translation import gettext_lazy as _


class MyUser(AbstractUser):
    email = models.EmailField(_('email address'), unique=True)

    def is_owner(self, obj=None):
        if not obj or obj.author != self.username:
            return False
        return True
