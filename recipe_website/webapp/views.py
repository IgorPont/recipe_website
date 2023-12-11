from django.shortcuts import render, get_object_or_404
from django.contrib.auth.mixins import LoginRequiredMixin, UserPassesTestMixin
from django.contrib.auth.models import User
from django.views.generic import (
    TemplateView, ListView, DetailView,
    CreateView, UpdateView, DeleteView
)
from .models import Recipe, Category
from .forms import RecipeForm
from django.urls import reverse_lazy
from django.contrib import messages
import logging

logger = logging.getLogger(__name__)


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

    def get_context_data(self, **kwargs):
        # Обработчик переменной 'categories' для меню категорий рецептов
        context = super().get_context_data(**kwargs)
        context['categories'] = Category.objects.all()
        return context


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

    def get_context_data(self, **kwargs):
        # Обработчик переменной 'categories' для меню категорий рецептов
        context = super().get_context_data(**kwargs)
        context['categories'] = Category.objects.all()
        return context


class RecipeByCategoryView(ListView):
    model = Recipe
    template_name = 'webapp/recipes_by_category.html'
    context_object_name = 'recipes'

    def get_queryset(self):
        category = get_object_or_404(Category, id=self.kwargs['category_id'])
        return Recipe.objects.filter(category=category)

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        context['category'] = get_object_or_404(Category, id=self.kwargs['category_id'])
        context['categories'] = Category.objects.all()
        return context


class RecipeDetailView(DetailView):
    """
    Отображение подробной информации о конкретном объекте модели Recipe
    """
    model = Recipe

    def get_context_data(self, **kwargs):
        # Обработчик переменной 'categories' для меню категорий рецептов
        context = super().get_context_data(**kwargs)
        context['categories'] = Category.objects.all()
        return context


class RecipeCreateView(LoginRequiredMixin, CreateView):
    """
    Создание новых объектов модели Recipe,
    где автором будет текущий аутентифицированный пользователь
    """
    model = Recipe
    form_class = RecipeForm

    def form_valid(self, form):
        form.instance.author = self.request.user
        result = super().form_valid(form)
        messages.success(self.request, 'Рецепт успешно добавлен.')
        return result

    def form_invalid(self, form):
        return super().form_invalid(form)

    def get_context_data(self, **kwargs):
        # Обработчик переменной 'categories' для меню категорий рецептов
        context = super().get_context_data(**kwargs)
        context['categories'] = Category.objects.all()
        return context


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
        form.instance.author = self.request.user
        result = super().form_valid(form)
        messages.success(self.request, 'Рецепт успешно обновлен.')
        return result

    def test_func(self):
        recipe = self.get_object()
        if self.request.user == recipe.author:
            return True
        return False

    def get_context_data(self, **kwargs):
        # Обработчик переменной 'categories' для меню категорий рецептов
        context = super().get_context_data(**kwargs)
        context['categories'] = Category.objects.all()
        return context


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

    def delete(self, request, *args, **kwargs):
        messages.success(self.request, 'Рецепт успешно удален.')
        return super().delete(request, *args, **kwargs)

    def get_context_data(self, **kwargs):
        # Обработчик переменной 'categories' для меню категорий рецептов
        context = super().get_context_data(**kwargs)
        context['categories'] = Category.objects.all()
        return context


class AboutView(TemplateView):
    """
    Отображение страницы с описанием о сайте (через класс)
    """
    template_name = 'webapp/about.html'
    extra_context = {'title': 'О клубе любителей готовить'}

    def get_context_data(self, **kwargs):
        # Обработчик переменной 'categories' для меню категорий рецептов
        context = super().get_context_data(**kwargs)
        context['categories'] = Category.objects.all()
        return context

# todo: Добавить свои обработчики ошибок 404, 500 и тд.
# todo: Дописать логирование
# todo: Дописать обработку исключений при работе с базой данных
# todo: Добавить детальное описание рецепта при клике по его заголовку + уменьшить также картинку
# todo: Добавить отображение категорий
