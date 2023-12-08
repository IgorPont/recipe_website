from django.shortcuts import render, get_object_or_404
from django.contrib.auth.mixins import LoginRequiredMixin, UserPassesTestMixin
from django.contrib.auth.models import User
from django.views.generic import (
    TemplateView, ListView, DetailView,
    CreateView, UpdateView, DeleteView
)
from .models import Recipe
from .forms import RecipeForm
from django.urls import reverse_lazy
import logging

logger = logging.getLogger(__name__)


# def home(request):
#     """
#     Отображение всех опубликованных рецептов (через функцию представления, для теста)
#     """
#     context = {
#         'recipes': Recipe.objects.all(),
#     }
#     return render(request, template_name='webapp/home.html', context=context)


# def about(request):
#     """
#     Отображение страницы с описанием о сайте (через функцию представления, для теста)
#     """
#     context = {
#         'title': 'О блоге любителей готовить'
#     }
#     return render(request, template_name='webapp/about.html', context=context)


class RecipeListView(ListView):
    """
    Отображает список объектов модели Recipe
    """
    model = Recipe
    template_name = 'webapp/home.html'
    context_object_name = 'recipes'
    # Сортировка объектов по дате публикации в убывающем порядке
    ordering = ['-created_date']
    # Пагинация постов с рецептами
    paginate_by = 6


class UserRecipeListView(ListView):
    """
    Отображает список объектов модели Recipe конкретного пользователя
    """
    model = Recipe
    template_name = 'webapp/user_recipes.html'
    context_object_name = 'recipes'
    paginate_by = 6

    def get_queryset(self):
        user = get_object_or_404(User, username=self.kwargs.get('username'))
        return Recipe.objects.filter(author=user).order_by('-created_date')


class RecipeDetailView(DetailView):
    """
    Отображение подробной информации о конкретном объекте модели Recipe
    """
    model = Recipe


class RecipeCreateView(LoginRequiredMixin, CreateView):
    """
    Создание новых объектов модели Recipe,
    где автором будет текущий аутентифицированный пользователь
    """
    # model = Recipe
    # fields = ['title', 'category', 'description',
    #           'ingredients', 'cooking_steps', 'cooking_time',
    #           'active', 'image', ]

    model = Recipe
    form_class = RecipeForm

    def form_valid(self, form):
        # print("Form is valid!")
        form.instance.author = self.request.user
        result = super().form_valid(form)
        # print("Recipe created successfully!")
        return result

    def form_invalid(self, form):
        # print("Form is invalid!")
        # print(form.errors)
        return super().form_invalid(form)


class RecipeUpdateView(LoginRequiredMixin, UserPassesTestMixin, UpdateView):
    """
    Обновление созданных объектов модели Recipe, при условии,
    что текущий пользователь является автором этих рецептов
    """
    model = Recipe
    fields = ['title', 'category', 'description',
              'ingredients', 'cooking_steps', 'cooking_time',
              'active', 'image', ]

    def form_valid(self, form):
        # print("Form is valid!")
        form.instance.author = self.request.user
        # print("Recipe updated successfully!")
        return super().form_valid(form)

    def test_func(self):
        recipe = self.get_object()
        if self.request.user == recipe.author:
            return True
        return False


class RecipeDeleteView(LoginRequiredMixin, UserPassesTestMixin, DeleteView):
    """
    Удаление объектов модели Recipe, при условии,
    что текущий пользователь является автором объекта
    """
    model = Recipe
    success_url = reverse_lazy('webapp-home')

    def test_func(self):
        recipe = self.get_object()
        if self.request.user == recipe.author:
            return True
        return False


class AboutView(TemplateView):
    """
    Отображение страницы с описанием о сайте (через класс)
    """
    template_name = 'webapp/about.html'
    extra_context = {'title': 'О клубе любителей готовить'}

# todo: Добавить свои обработчики ошибок 404, 500 и тд.
# todo: Дописать логирование
# todo: Дописать обработку исключений при работе с базой данных
# todo: Разместить по два в ряд рецепта на главной и странице рецептов пользователя
# todo: Добавить детальное описание рецепта при клиеке по его заголовку
