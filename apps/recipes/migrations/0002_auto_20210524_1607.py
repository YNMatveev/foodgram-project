# Generated by Django 3.2.2 on 2021-05-24 16:07

from django.db import migrations, models
import multiselectfield.db.fields


class Migration(migrations.Migration):

    dependencies = [
        ('recipes', '0001_initial'),
    ]

    operations = [
        migrations.AlterField(
            model_name='recipe',
            name='slug',
            field=models.SlugField(blank=True, unique=True, verbose_name='Slug'),
        ),
        migrations.AlterField(
            model_name='recipe',
            name='tags',
            field=multiselectfield.db.fields.MultiSelectField(choices=[('завтрак', 'завтрак'), ('обед', 'обед'), ('ужин', 'ужин')], default='завтрак', max_length=100, verbose_name='Tags'),
        ),
    ]