import csv

from django.core.management.base import BaseCommand
from recipes.models import Ingredient

duplicate = ['пекарский порошок', 'стейк семги']


class Command(BaseCommand):
    help = 'Populate Ingredients Database'

    def add_arguments(self, parser):
        parser.add_argument('csv_file', type=str)

    def handle(self, *args, **options):

        with open(options['csv_file'], 'rt') as f:
            reader = csv.reader(f, dialect='excel', delimiter=',')

            for row in reader:
                name, units = row

                if units == '' or name in duplicate:
                    units = 'г'
                ingredient, created = Ingredient.objects.get_or_create(
                    name=name.lower(), units=units
                )
