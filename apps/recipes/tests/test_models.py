from django.test import TestCase
from recipes.models import Ingredient
from django.db import IntegrityError


class IngredientModelTest(TestCase):

    @classmethod
    def setUpClass(cls):
        super().setUpClass()
        cls.ingredient = Ingredient.objects.create(name='Помидоры', units='г')

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
            duplicate_name = Ingredient.objects.create(name='Помидоры',
                                                       units='шт')

    def test_object_name_is_name_comma_unit(self):
        ingredient = IngredientModelTest.ingredient
        expected_object_name = (f'{ingredient.name}, {ingredient.units}')
        self.assertEquals(expected_object_name, str(ingredient))
