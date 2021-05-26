from django.contrib.auth import get_user_model
from django.core.validators import MinValueValidator
from django.db import models
from django.db.models import Max
from django.urls import reverse
from multiselectfield import MultiSelectField
from pytils.translit import slugify
from stdimage import StdImageField

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
                               verbose_name='Автор')

    title = models.CharField(max_length=100, verbose_name='Название')
    image = StdImageField(upload_to='recipes/', delete_orphans=True,
                          verbose_name='Изображение')

    description = models.TextField(verbose_name='Рецепт')

    ingredients = models.ManyToManyField(
        'recipes.Ingredient', through='recipes.IngredientRecipeMap',
        related_name='recipes', verbose_name='Необходимые ингредиенты')

    tags = MultiSelectField(verbose_name='Tags', choices=Tag.choices,
                            default=Tag.BREAKFAST, max_length=30)

    cooking_time = models.PositiveIntegerField(
        verbose_name='Время приготовления в минутах',
        validators=[MinValueValidator(1)]
    )

    slug = models.SlugField(verbose_name='Slug', blank=True, db_index=True)

    created = models.DateTimeField(verbose_name='Дата создания',
                                   auto_now_add=True, db_index=True)

    modified = models.DateTimeField(verbose_name='Дата изменения',
                                    auto_now=True)

    class Meta:
        ordering = ['-created']
        verbose_name = 'Рецепт'
        verbose_name_plural = 'Рецепты'

    def __str__(self):
        return self.title

    def save(self, *args, **kwargs):
        self.slug = slugify(self.title)
        super().save(*args, **kwargs)

    def get_absolute_url(self):
        return reverse('recipes:recipe_details',
                       kwargs={'slug': self.slug, 'id': self.id})


class Ingredient(models.Model):

    name = models.CharField(verbose_name='Название', max_length=60,
                            unique=True, db_index=True)

    units = models.CharField(verbose_name='Ед.измерения',
                             max_length=10)

    class Meta:
        verbose_name = 'Ингредиент'
        verbose_name_plural = 'Ингредиент'


    def __str__(self):
        return f'{self.name}, {self.units}'


class IngredientRecipeMap(models.Model):

    ingredient = models.ForeignKey(Ingredient, on_delete=models.DO_NOTHING,
                                   verbose_name='Ингредиент')
    recipe = models.ForeignKey(Recipe, on_delete=models.CASCADE,
                               related_name='required_ingredients',
                               verbose_name='Рецепт')
    
    quantity = models.PositiveIntegerField(validators=[MinValueValidator(1)],
                                           verbose_name='Количество')

    class Meta:
        verbose_name = 'Ингредиенты в Рецептах'
        verbose_name_plural = 'Ингредиенты в Рецептах'
        constraints = [
            models.UniqueConstraint(fields=['recipe', 'ingredient'],
                                    name='unique_ingredient')
        ]

    def __str__(self):
        return (f'{self.ingredient.name.capitalize()} - {self.quantity} '
                f'{self.ingredient.units}.')


class Favorite(models.Model):

    chooser = models.ForeignKey(User, verbose_name='Пользователь',
                                related_name='favorites',
                                on_delete=models.CASCADE)
    recipe = models.ForeignKey(Recipe, verbose_name='Рецепт',
                               related_name='favorites',
                               on_delete=models.CASCADE)

    class Meta:
        verbose_name = 'Избранные рецепты'
        verbose_name_plural = 'Избранные рецепты'
        
        constraints = [
            models.UniqueConstraint(fields=['chooser', 'recipe'],
                                    name='unique_favorites')
        ]


class Subscribe(models.Model):

    subscriber = models.ForeignKey(User, verbose_name='Пользователь',
                                   related_name='recipe_authors',
                                   on_delete=models.CASCADE)

    author = models.ForeignKey(User, verbose_name='Автор',
                               related_name='subscribers',
                               on_delete=models.CASCADE)

    class Meta:
        verbose_name = 'Подписка'
        verbose_name_plural = 'Подписки'
        constraints = [
            models.UniqueConstraint(fields=['subscriber', 'author'],
                                    name='unique_subscribe')
        ]
