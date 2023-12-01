from .models import Category, Recipe
from django.shortcuts import render, redirect
import logging

logger = logging.getLogger(__name__)


def home(request):
    """Главная страница со всеми опубликованными рецептами"""
    context = {
        'recipes': Recipe.objects.all(),
    }
    return render(request, template_name='webapp/home.html', context=context)


def about(request):
    """Страница с описанием о сайте"""
    context = {
        'title': 'О блоге любителей готовить'
    }
    return render(request, template_name='webapp/about.html', context=context)

# todo: Добавить свои обработчики ошибок 404, 500 и тд.
