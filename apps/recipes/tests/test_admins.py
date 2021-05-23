from django.contrib.auth import get_user_model
from django.test import TestCase
from recipes.admin import RecipeAdmin
from recipes.models import Favorite, Recipe

User = get_user_model()


class RecipeAdminTest(TestCase):

    @classmethod
    def setUpClass(cls):
        super().setUpClass()
        cls.author = User.objects.create_user(username='John',
                                              email='aa@aa.ru')
        cls.user = User.objects.create_user(username='User',
                                            email='bb@bb.ru')
        cls.recipe = Recipe.objects.create(
            author=cls.author, title='Стейк', tags=Recipe.Tag.DINNER,
            description='Порядок приготовления', cooking_time=20
        )
        cls.favorite = Favorite.objects.create(chooser=cls.user,
                                               recipe=cls.recipe)

    def test_count_favorites(self):
        admin_function_result = RecipeAdmin.count_times_in_favorite(
            RecipeAdmin, obj=self.recipe)
        self.assertEquals(admin_function_result, 1)
