from django.contrib.auth import get_user_model
from django.db import models

User = get_user_model()


class Purchase(models.Model):

    user = models.OneToOneField(User, on_delete=models.CASCADE,
                                related_name='carts',
                                verbose_name='Пользователь')

    shopping_list = models.JSONField(verbose_name='Список рецептов',
                                     default=list)

    class Meta:
        verbose_name = 'Список покупок'
        verbose_name_plural = 'Списки покупок'

    def __str__(self):
        return f'Список покупок {self.user}'
