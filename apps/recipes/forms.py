from django.forms import ModelForm, ValidationError

from recipes.models import Ingredient, IngredientRecipeMap, Recipe


class RecipeForm(ModelForm):

    class Meta:
        model = Recipe
        fields = ('title', 'tags', 'ingredients', 'cooking_time',
                  'description', 'image',)

        error_messages = {
            'title': {'required': '"Название рецепта" обязательное поле'},
            'tags': {'required': '"Теги" обязательное поле'},
            'cooking_time': {
                'required': '"Время приготовления" обязательное поле',
                'min_value': '"Время приготовления" должно быть положительным',
            },
            'description': {'required': '"Описание" обязательное поле'},
            'image': {'required': '"Картинка" обязательное поле'},
        }

        labels = {
            'title': 'Название рецепта',
            'tags': 'Теги',
            'ingredients': 'Ингредиенты',
            'cooking_time': 'Время приготовления',
            'description': 'Описание',
            'image': 'Загрузить фото',
        }

    def __init__(self, *args, **kwargs):
        super(RecipeForm, self).__init__(*args, **kwargs)
        self.fields['ingredients'].required = False

    def clean_ingredients(self):
        data = self.cleaned_data['ingredients']
        all_ingredients = Ingredient.objects.values_list('name', flat=True)

        if 'nameIngredient' not in ' '.join(self.data.keys()):
            raise ValidationError(
                'В рецепт нужно добавить минимум один "Ингредиент"'
            )

        candidates = [value for key, value in self.data.items()
                      if 'nameIngredient' in key]
        contains_duplicates = any(candidates.count(element) > 1
                                  for element in candidates)

        if contains_duplicates:
            raise ValidationError('"Игредиенты" должны быть уникальными. '
                                  'Повторы запрещены')

        recipe_ingredients = []
        for key, value in self.data.items():

            if 'nameIngredient' in key:
                if value not in all_ingredients:
                    raise ValidationError(
                        f'{value}: Ингредиенты должны быть выбраны из списка')
                ingredient_name = value

            if 'valueIngredient' in key:
                ingredient_value = value
                recipe_ingredients.append(
                    (Ingredient.objects.get(name=ingredient_name),
                     ingredient_value)
                )

        data = recipe_ingredients
        return data

    def save(self, commit=True):

        recipe = super().save(commit=False)

        if commit:
            recipe.save()
            current_ingredients = recipe.required_ingredients.all()
            if current_ingredients.exists():
                current_ingredients.delete()

            ingredients = self.cleaned_data.get('ingredients', [])
            IngredientRecipeMap.objects.bulk_create(
                [
                    IngredientRecipeMap(recipe=recipe, ingredient=ingredient,
                                        quantity=quantity)
                    for (ingredient, quantity) in ingredients
                ]
            )

        return recipe
