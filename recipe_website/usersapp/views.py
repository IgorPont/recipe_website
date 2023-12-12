from django.shortcuts import render, redirect
from django.contrib import messages
from django.contrib.auth.decorators import login_required
from django.contrib.auth.views import LoginView, LogoutView
from .forms import UserRegisterForm, UserUpdateForm, ProfileUpdateForm
from webapp.models import Category


def register(request):
    """
    Регистрация пользователя на сайте
    """
    if request.method == 'POST':
        form = UserRegisterForm(request.POST)
        if form.is_valid():
            form.save()
            username = form.cleaned_data.get('username')
            messages.success(request, f'{username}, аккаунт создан! Можно авторизоваться в личном кабинете.')
            return redirect('login')
    else:
        form = UserRegisterForm()

    categories = Category.objects.all()

    context = {
        'form': form,
        'categories': categories
    }

    return render(request, 'usersapp/register.html', context=context)


@login_required
def profile(request):
    """
    Изменение данных профиля пользователем на сайте
    """
    if request.method == 'POST':
        u_form = UserUpdateForm(request.POST, instance=request.user)
        p_form = ProfileUpdateForm(request.POST,
                                   request.FILES,
                                   instance=request.user.profile)
        if u_form.is_valid() and p_form.is_valid():
            u_form.save()
            p_form.save()
            messages.success(request, f'Ваш профиль успешно обновлен.')
            return redirect('profile')
    else:
        u_form = UserUpdateForm(instance=request.user)
        p_form = ProfileUpdateForm(instance=request.user.profile)

    categories = Category.objects.all()

    context = {
        'u_form': u_form,
        'p_form': p_form,
        'categories': categories
    }

    return render(request, 'usersapp/profile.html', context=context)


class CustomLoginView(LoginView):
    """
    Обработчик переменной 'categories' для меню категорий рецептов на странице авторизации
    """
    template_name = 'usersapp/login.html'

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        context['categories'] = Category.objects.all()
        return context


class CustomLogoutView(LogoutView):
    """
    Обработчик переменной 'categories' для меню категорий рецептов на странице успешного выхода
    """
    template_name = 'usersapp/logout.html'

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        context['categories'] = Category.objects.all()
        return context
