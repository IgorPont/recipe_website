from django.contrib import admin
from .models import Category, Recipe

admin.site.site_title = 'Админ-панель сайта ВкуснаяЕда'
admin.site.site_header = 'Админ-панель сайта ВкуснаяЕда'

admin.site.register(Category)
admin.site.register(Recipe)
