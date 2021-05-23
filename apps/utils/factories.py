from random import choice

import factory
from django.contrib.auth import get_user_model
from factory import fuzzy
from factory.django import DjangoModelFactory

from recipes.models import Ingredient, IngredientRecipeMap, Recipe

User = get_user_model()


class UserFactory(DjangoModelFactory):
    class Meta:
        model = User

    id = factory.sequence(lambda n: n)
    username = factory.Faker('user_name')
    email = factory.Faker('email')
    password = 'secret'

    @factory.lazy_attribute
    def last_name(self):
        if choice([True, False]):
            return factory.faker.faker.Faker().last_name()
        else:
            return ''

    @factory.lazy_attribute
    def first_name(self):
        if choice([True, False]):
            return factory.faker.faker.Faker().first_name()
        else:
            return ''

    @classmethod
    def _create(cls, model_class, *args, **kwargs):
        """Override the default ``_create`` with our custom call."""
        manager = cls._get_manager(model_class)
        # The default would use ``manager.create(*args, **kwargs)``
        return manager.create_user(*args, **kwargs)


#  class BaseRecipeFactory(DjangoModelFactory):
class RecipeFactory(DjangoModelFactory):
    class Meta:
        model = Recipe

    author = factory.SubFactory(UserFactory)
    title = factory.Faker('bs')
    created = factory.Faker('date_time_this_year')
    cooking_time = fuzzy.FuzzyInteger(5, 90)
    image = factory.django.ImageField(
        from_path=('static_files/images/testCardImg.png'))
    #  tags
    description = factory.Faker('paragraph', nb_sentences=9,
                                variable_nb_sentences=True)

    #  ingridients
    #  slug
    #  modified


class IngredientRecipeMapFactory(DjangoModelFactory):
    class Meta:
        model = IngredientRecipeMap
        django_get_or_create = ('recipe',)

    recipe = factory.SubFactory(RecipeFactory)
    quantity = fuzzy.FuzzyInteger(1, 1000)

    @factory.lazy_attribute
    def ingredient(self):
        return choice(Ingredient.objects.all())
