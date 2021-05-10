from django.db import models
from django.contrib.auth import get_user_model
from stdimage import StdImageField
from multiselectfield import MultiSelectField
from pytils.translit import slugify

User = get_user_model()


def get_abstract_user():
    return User.objects.get_or_create(username='deleted')[0]


class Recipe(models.Model):

    class Tag(models.TextChoices):
        BREAKFAST = 'завтрак', 'завтрак'
        LUNCH = 'обед', 'обед'
        DINNER = 'ужин', 'ужин'

    author = models.ForeignKey(User, on_delete=models.SET(get_abstract_user),
                               related_name='recipes',
                               verbose_name='Recipe Author')

    title = models.CharField(max_length=100, verbose_name='Recipe Title')
    image = StdImageField(upload_to='recipes/', delete_orphans=True,
                          verbose_name='Photo of the dish')

    description = models.TextField(verbose_name='Recipe Description')

    ingredients = models.ManyToManyField(
        'recipes.Ingredient', through='recipes.IngredientRecipeMap',
        related_name='recipes', verbose_name='Required ingredients')

    tag = MultiSelectField(verbose_name='Tags', choices=Tag.choices)

    cooking_time = models.PositiveIntegerField(
        verbose_name='Cooking time, minutes')

    slug = models.SlugField(max_length=200, unique=True, verbose_name='Slug')

    created = models.DateTimeField(verbose_name='Published Date',
                                   auto_now_add=True)

    modified = models.DateTimeField(verbose_name='Modified Date',
                                    auto_now=True)

    def __str__(self):
        return self.title

    @property
    def get_times_to_favorites(self):
        return self.favorites.count()

    get_times_to_favorites.fget.short_description = (
        'Times recipe add in favorites')

    def save(self, *args, **kwargs):
        suffix = Recipe.objects.count() + 1
        self.slug = slugify(self.title)[:100] + '-' + str(suffix)
        super().save(*args, **kwargs)


class Ingredient(models.Model):

    name = models.CharField(verbose_name='Name', max_length=60,
                            unique=True, db_index=True)

    units = models.CharField(verbose_name='Units of measurements',
                             max_length=10)

    def __str__(self):
        return f'{self.name}, {self.units}'


class IngredientRecipeMap(models.Model):

    ingredient = models.ForeignKey(Ingredient, on_delete=models.DO_NOTHING)
    recipe = models.ForeignKey(Recipe, on_delete=models.CASCADE)
    quantity = models.PositiveIntegerField()


class Favorite(models.Model):

    chooser = models.ForeignKey(User, verbose_name='Chooser',
                                related_name='favorites',
                                on_delete=models.CASCADE)
    recipe = models.ForeignKey(Recipe, verbose_name='Favorite recipe',
                               related_name='favorites',
                               on_delete=models.CASCADE)

    class Meta:
        constraints = [
            models.UniqueConstraint(fields=['chooser', 'recipe'],
                                    name='unique_favorites')
        ]


class Subscribe(models.Model):

    subscriber = models.ForeignKey(User, verbose_name='Subscriber',
                                   related_name='recipe_authors',
                                   on_delete=models.CASCADE)

    author = models.ForeignKey(User, verbose_name='Author',
                               related_name='subscribers',
                               on_delete=models.CASCADE)

    class Meta:
        constraints = [
            models.UniqueConstraint(fields=['subscriber', 'author'],
                                    name='unique_subscribe')
        ]
