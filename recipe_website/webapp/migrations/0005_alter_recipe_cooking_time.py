# Generated by Django 4.2.8 on 2023-12-12 20:18

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('webapp', '0004_alter_recipe_cooking_time_alter_recipe_image'),
    ]

    operations = [
        migrations.AlterField(
            model_name='recipe',
            name='cooking_time',
            field=models.DurationField(verbose_name='Время приготовления (мин:сек)'),
        ),
    ]