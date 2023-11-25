from django.db import models
from django.contrib.auth.models import User
from django.utils import timezone


class Category(models.Model):
    name = models.CharField(max_length=100, verbose_name="Название категории")

    def __str__(self):
        return self.name


class Recipe(models.Model):
    title = models.CharField(max_length=150, verbose_name="Заголовок рецепта")
    category = models.ForeignKey(Category, on_delete=models.CASCADE, verbose_name="Категория")
    description = models.TextField(verbose_name="Описание рецепта")
    ingredients = models.TextField(verbose_name="Ингредиенты")
    cooking_steps = models.TextField(verbose_name="Шаги приготовления")
    cooking_time = models.TimeField(verbose_name="Время приготовления")
    image = models.ImageField(upload_to='images/', verbose_name="Изображения")
    user = models.ForeignKey(User, on_delete=models.CASCADE)
    active = models.BooleanField(default=True, verbose_name="Статус активности")
    created_date = models.DateTimeField(default=timezone.now, verbose_name="Дата создания")

    def __str__(self):
        return self.title
