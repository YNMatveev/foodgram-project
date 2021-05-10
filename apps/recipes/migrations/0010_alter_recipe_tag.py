# Generated by Django 3.2.2 on 2021-05-09 17:02

from django.db import migrations
import multiselectfield.db.fields


class Migration(migrations.Migration):

    dependencies = [
        ('recipes', '0009_alter_recipe_image'),
    ]

    operations = [
        migrations.AlterField(
            model_name='recipe',
            name='tag',
            field=multiselectfield.db.fields.MultiSelectField(choices=[('завтрак', 'завтрак'), ('обед', 'обед'), ('ужин', 'ужин')], max_length=17),
        ),
    ]
