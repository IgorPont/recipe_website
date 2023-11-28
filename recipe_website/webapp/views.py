from django.shortcuts import render
from django.views.generic import ListView
from .models import Category, Recipe
from django.contrib.auth.forms import UserCreationForm
from django.contrib.auth import login
from django.shortcuts import render, redirect
from django.http import HttpResponse
from django.contrib.auth.decorators import login_required
import logging

logger = logging.getLogger(__name__)


# def register(request):
#     if request.method == 'POST':
#         form = UserCreationForm(request.POST)
#         if form.is_valid():
#             user = form.save()
#             # Автоматически входить после успешной регистрации
#             login(request, user)
#             return redirect('index')  # Перенаправление на вашу страницу после регистрации
#     else:
#         form = UserCreationForm()
#     return render(request, 'registration/register.html', {'form': form})


def home(request):
    """Главная страница со всеми опубликованными рецептами"""

    recipes = [
        {
            'author': 'Администратор',
            'created_date': '28.11.2023',
            'title': 'Заголовок рецепта',

            # todo: Добавить изодбражение блюда

            'ingredients': 'Игридиенты блюда.',

        },
        {
            'author': 'Пользователь',
            'created_date': '28.11.2023',
            'title': 'Заголовок рецепта',

            # todo: Добавить изодбражение блюда

            'ingredients': 'Игридиенты блюда.',
        }
    ]

    context = {
        'recipes': recipes,
    }
    return render(request, template_name='webapp/home.html', context=context)


def about(request):
    """Страница с описанием о сайте"""

    context = {
        'title': 'О блоге любителей готовить'
    }
    return render(request, template_name='webapp/about.html', context=context)
