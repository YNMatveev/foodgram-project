# Generated by Django 3.2.2 on 2021-05-27 17:34

from django.conf import settings
import django.core.validators
from django.db import migrations, models
import django.db.models.deletion
import django.db.models.expressions
import multiselectfield.db.fields
import recipes.models
import stdimage.models


class Migration(migrations.Migration):

    initial = True

    dependencies = [
        migrations.swappable_dependency(settings.AUTH_USER_MODEL),
    ]

    operations = [
        migrations.CreateModel(
            name='Ingredient',
            fields=[
                ('id', models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('name', models.CharField(db_index=True, max_length=60, unique=True, verbose_name='Название')),
                ('units', models.CharField(max_length=10, verbose_name='Ед.измерения')),
            ],
            options={
                'verbose_name': 'Ингредиент',
                'verbose_name_plural': 'Ингредиент',
            },
        ),
        migrations.CreateModel(
            name='IngredientRecipeMap',
            fields=[
                ('id', models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('quantity', models.PositiveIntegerField(validators=[django.core.validators.MinValueValidator(1)], verbose_name='Количество')),
                ('ingredient', models.ForeignKey(on_delete=django.db.models.deletion.DO_NOTHING, to='recipes.ingredient', verbose_name='Ингредиент')),
            ],
            options={
                'verbose_name': 'Ингредиенты в Рецептах',
                'verbose_name_plural': 'Ингредиенты в Рецептах',
            },
        ),
        migrations.CreateModel(
            name='Subscribe',
            fields=[
                ('id', models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('author', models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, related_name='subscribers', to=settings.AUTH_USER_MODEL, verbose_name='Автор')),
                ('subscriber', models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, related_name='recipe_authors', to=settings.AUTH_USER_MODEL, verbose_name='Пользователь')),
            ],
            options={
                'verbose_name': 'Подписка',
                'verbose_name_plural': 'Подписки',
            },
        ),
        migrations.CreateModel(
            name='Recipe',
            fields=[
                ('id', models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('title', models.CharField(max_length=100, verbose_name='Название')),
                ('image', stdimage.models.StdImageField(upload_to='recipes/', verbose_name='Изображение')),
                ('description', models.TextField(verbose_name='Рецепт')),
                ('tags', multiselectfield.db.fields.MultiSelectField(choices=[('завтрак', 'завтрак'), ('обед', 'обед'), ('ужин', 'ужин')], default='завтрак', max_length=30, verbose_name='Tags')),
                ('cooking_time', models.PositiveIntegerField(validators=[django.core.validators.MinValueValidator(1)], verbose_name='Время приготовления в минутах')),
                ('slug', models.SlugField(blank=True, verbose_name='Слаг')),
                ('created', models.DateTimeField(auto_now_add=True, db_index=True, verbose_name='Дата создания')),
                ('modified', models.DateTimeField(auto_now=True, verbose_name='Дата изменения')),
                ('author', models.ForeignKey(on_delete=models.SET(recipes.models.get_abstract_user), related_name='recipes', to=settings.AUTH_USER_MODEL, verbose_name='Автор')),
                ('ingredients', models.ManyToManyField(related_name='recipes', through='recipes.IngredientRecipeMap', to='recipes.Ingredient', verbose_name='Необходимые ингредиенты')),
            ],
            options={
                'verbose_name': 'Рецепт',
                'verbose_name_plural': 'Рецепты',
                'ordering': ['-created'],
            },
        ),
        migrations.AddField(
            model_name='ingredientrecipemap',
            name='recipe',
            field=models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, related_name='required_ingredients', to='recipes.recipe', verbose_name='Рецепт'),
        ),
        migrations.CreateModel(
            name='Favorite',
            fields=[
                ('id', models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('chooser', models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, related_name='favorites', to=settings.AUTH_USER_MODEL, verbose_name='Пользователь')),
                ('recipe', models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, related_name='favorites', to='recipes.recipe', verbose_name='Рецепт')),
            ],
            options={
                'verbose_name': 'Избранные рецепты',
                'verbose_name_plural': 'Избранные рецепты',
            },
        ),
        migrations.AddConstraint(
            model_name='subscribe',
            constraint=models.UniqueConstraint(fields=('subscriber', 'author'), name='unique_subscribe'),
        ),
        migrations.AddConstraint(
            model_name='subscribe',
            constraint=models.CheckConstraint(check=models.Q(('author', django.db.models.expressions.F('subscriber')), _negated=True), name='author_subscriber_not_equal'),
        ),
        migrations.AddConstraint(
            model_name='ingredientrecipemap',
            constraint=models.UniqueConstraint(fields=('recipe', 'ingredient'), name='unique_ingredient'),
        ),
        migrations.AddConstraint(
            model_name='favorite',
            constraint=models.UniqueConstraint(fields=('chooser', 'recipe'), name='unique_favorites'),
        ),
    ]