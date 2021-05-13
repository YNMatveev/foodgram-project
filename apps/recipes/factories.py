from random import choice, randint

import factory
from django.contrib.auth import get_user_model
from factory import fuzzy
from factory.django import DjangoModelFactory

from recipes.models import Ingredient, IngredientRecipeMap, Recipe

User = get_user_model()


# Defining a factory
class UserFactory(DjangoModelFactory):
    class Meta:
        model = User
    username = factory.Faker('user_name')
    email = factory.Faker('email')
    password = 'secret'

    #  first_name = factory.Faker('first_name')
    #  last_name = factory.Faker('last_name')

    @classmethod
    def _create(cls, model_class, *args, **kwargs):
        """Override the default ``_create`` with our custom call."""
        manager = cls._get_manager(model_class)
        # The default would use ``manager.create(*args, **kwargs)``
        return manager.create_user(*args, **kwargs)


class BaseRecipeFactory(DjangoModelFactory):
    class Meta:
        model = Recipe

    author = factory.SubFactory(UserFactory)
    title = factory.Faker('bs')
    created = factory.Faker('date_time_this_year')
    cooking_time = fuzzy.FuzzyInteger(5, 90)
    image = factory.django.ImageField(
        from_path=('/Users/morf/Dev/course5_Diploma/foodgram-project'
                   '/static_files/images/testCardImg.png'))
    #  tags
    description = factory.Faker('paragraph', nb_sentences=3,
                                variable_nb_sentences=True)

    #  ingridients
    #  slug
    #  modified


class IngredientRecipeMapFactory(DjangoModelFactory):
    class Meta:
        model = IngredientRecipeMap

    recipe = factory.SubFactory(BaseRecipeFactory)
    quantity = fuzzy.FuzzyInteger(50, 500)

    @factory.lazy_attribute
    def ingredient(self):
        return choice(Ingredient.objects.all())


class RecipeFactory(BaseRecipeFactory):

    for _ in range(randint(3, 10)):
        ingredient = factory.RelatedFactory(
            IngredientRecipeMapFactory,
            factory_related_name='recipe')
