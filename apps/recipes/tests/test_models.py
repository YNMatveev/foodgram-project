from django.test import TestCase
from recipes.models import Ingredient, Recipe, Favorite, Subscribe
from django.db import IntegrityError
from django.contrib.auth import get_user_model

User = get_user_model()


def create_test_recipe(author, title):
    return Recipe.objects.create(
        author=author, title=title, tag=Recipe.Tag.DINNER,
        description='Порядок приготовления', cooking_time=20
    )


class IngredientModelTest(TestCase):

    @classmethod
    def setUpClass(cls):
        super().setUpClass()
        cls.ingredient = Ingredient.objects.create(name='помидоры', units='г')

    def test_verbose_name(self):
        ingredient = IngredientModelTest.ingredient
        field_verboses = {
            'name': 'Name',
            'units': 'Units of measurements'
        }

        for field, expected_value in field_verboses.items():
            with self.subTest(field=field):
                self.assertEquals(
                    ingredient._meta.get_field(field).verbose_name,
                    expected_value
                )

    def test_max_length(self):
        ingredient = IngredientModelTest.ingredient
        field_max_length = {
            'name': 60,
            'units': 10
        }

        for field, expected_value in field_max_length.items():
            with self.subTest(field=field):
                self.assertEquals(
                    ingredient._meta.get_field(field).max_length,
                    expected_value
                )

    def test_name_unique(self):
        with self.assertRaises(IntegrityError):
            _ = Ingredient.objects.create(name='помидоры', units='шт')

    def test_object_name_is_name_comma_unit(self):
        ingredient = IngredientModelTest.ingredient
        expected_object_name = (f'{ingredient.name}, {ingredient.units}')
        self.assertEquals(expected_object_name, str(ingredient))


class RecipeModelTest(TestCase):

    @classmethod
    def setUpClass(cls):
        super().setUpClass()

    def setUp(self):
        self.author = User.objects.create_user(username='John')
        self.recipe = create_test_recipe(author=self.author, title='Стейк')

    def test_verbose_name(self):

        field_verboses = {
            'title': 'Recipe Title',
            'author': 'Recipe Author',
            'description': 'Recipe Description',
            'ingredients': 'Required ingredients',
            'image': 'Photo of the dish',
            'tag': 'Tags',
            'cooking_time': 'Cooking time, minutes',
            'slug': 'Slug',
            'created': 'Published Date',
            'modified': 'Modified Date',
        }

        for field, expected_value in field_verboses.items():
            with self.subTest(field=field):
                self.assertEquals(
                    self.recipe._meta.get_field(field).verbose_name,
                    expected_value
                )

    def test_object_name_is_title(self):
        recipe = self.recipe
        expected_object_name = recipe.title
        self.assertEquals(expected_object_name, str(recipe))

    def test_slugify(self):
        recipe = self.recipe
        slug = recipe.slug
        self.assertEquals(slug, 'stejk-1')

    def test_slug_max_length(self):
        new_recipe = create_test_recipe(self.author, title='ш' * 100)
        self.assertEquals(new_recipe.slug, 'sh' * 50 + '-2')

    def test_recipe_author_change_to_deleted_after_delete_author(self):
        self.author.delete()
        self.recipe.refresh_from_db()
        self.assertEquals(self.recipe.author.username, 'deleted')

    def test_counter_recipe_in_favorites(self):
        user = User.objects.create_user('Current_user')
        _ = Favorite.objects.create(chooser=user, recipe=self.recipe)
        expected_value = 1
        counter = self.recipe.get_times_to_favorites
        self.assertEquals(counter, expected_value)


class FavoriteModelTest(TestCase):

    @classmethod
    def setUpClass(cls):
        super().setUpClass()
        cls.author = User.objects.create_user('John')
        cls.user = User.objects.create_user('Current_user')
        cls.recipe = create_test_recipe(cls.author, 'Стейк')
        cls.favorite = Favorite.objects.create(chooser=cls.user,
                                               recipe=cls.recipe)

    def test_verbose_name(self):

        field_verbose = {
            'chooser': 'Chooser',
            'recipe': 'Favorite recipe',
        }

        for field, expected_value in field_verbose.items():
            with self.subTest(field=field):
                self.assertEquals(
                    self.favorite._meta.get_field(field).verbose_name,
                    expected_value
                )

    def test_favorite_unique(self):
        with self.assertRaises(IntegrityError):
            _ = Favorite.objects.create(chooser=self.user, recipe=self.recipe)


class SubscribeModelTest(TestCase):

    @classmethod
    def setUpClass(cls):
        super().setUpClass()
        cls.author = User.objects.create_user('Author')
        cls.user = User.objects.create_user('Subscriber')
        cls.subscribe = Subscribe.objects.create(subscriber=cls.user,
                                                 author=cls.author)

    def test_verbose_name(self):

        field_verboses = {
            'author': 'Author',
            'subscriber': 'Subscriber'
        }

        for field, expected_value in field_verboses.items():
            with self.subTest(field=field):
                self.assertEquals(
                    self.subscribe._meta.get_field(field).verbose_name,
                    expected_value
                )

    def test_unique_subscribe(self):
        with self.assertRaises(IntegrityError):
            _ = Subscribe.objects.create(subscriber=self.user,
                                         author=self.author)
