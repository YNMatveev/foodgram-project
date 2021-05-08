from django.db import models

"""
class Recipe(models.Model):

    author = None
    title = None
    image = None
    description = None
    ingredients = None
    tag = None
    cooking_time = None
    slug = None
"""


class Ingredient(models.Model):

    name = models.CharField(verbose_name='Name', max_length=60,
                            unique=True, db_index=True)

    units = models.CharField(verbose_name='Units of measurements',
                             max_length=10)

    def __str__(self):
        return f'{self.name}, {self.units}'


"""
class IngredietRecipeMap(models.Model):

    ingridient = None
    recipe = None
    quantity = None


class Favorite(models.Model):

    user = None
    recipe = None


class Subscribe(models.Model):

    subscriber = None
    author = None
"""
