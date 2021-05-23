import itertools
import random

from django.contrib.auth import get_user_model
from django.core.management.base import BaseCommand
from django.db import transaction
from recipes.models import Favorite, IngredientRecipeMap, Recipe, Subscribe
from utils.factories import (IngredientRecipeMapFactory, RecipeFactory,
                             UserFactory)

User = get_user_model()

NUM_USERS = 10
NUM_SUBSCRIBERS = 3
NUM_FAVORITES = 25
RECIPE_PER_TAGS = 3
MIN_INGREDIENTS = 3
MAX_INGREDIENTS = 10


class Command(BaseCommand):
    help = "Generates test data"

    @transaction.atomic
    def handle(self, *args, **kwargs):
        self.stdout.write("Deleting old data...")
        models = [Recipe, Favorite, Subscribe, IngredientRecipeMap]
        for model in models:
            model.objects.all().delete()
        User.objects.exclude(id=1).delete()

        self.stdout.write("Creating new data...")

        default_tags = [tag for tag in Recipe.Tag]
        tags_variations = []
        for count in range(1, len(default_tags) + 1):
            for subset in itertools.combinations(default_tags, count):
                tags_variations.append(', '.join(list(subset)))

        # Create all the users
        UserFactory.reset_sequence(2)
        users = UserFactory.create_batch(NUM_USERS)

        # Create all the recipes
        for user in users:
            for tag in tags_variations:
                for _ in range(RECIPE_PER_TAGS):
                    recipe = RecipeFactory(author=user, tags=tag)
                    number_ingredients = random.randint(
                        MIN_INGREDIENTS, MAX_INGREDIENTS)
                    for __ in range(number_ingredients):
                        map_obj = IngredientRecipeMapFactory(recipe=recipe)
                        recipe.ingredients.add(map_obj.ingredient)

        for user in User.objects.exclude(id=1):
            recipes = list(Recipe.objects.exclude(author=user))
            to_favorite = random.sample(recipes, NUM_FAVORITES)
            Favorite.objects.bulk_create([
                Favorite(chooser=user, recipe=recipe)
                for recipe in to_favorite
            ])
            authors = list(User.objects.exclude(id=1, username=user.username))
            for_subscribe = random.sample(authors, NUM_SUBSCRIBERS)
            Subscribe.objects.bulk_create([
                Subscribe(subscriber=user, author=author)
                for author in for_subscribe
            ])
