from django.db import models
from django.contrib.auth.models import User
from webapp.models import user_directory_path


class Profile(models.Model):
    user = models.OneToOneField(User, on_delete=models.CASCADE, verbose_name="Пользователь сайта")
    image = models.ImageField(default='default.jpg', upload_to=user_directory_path, verbose_name="Аватар")

    def __str__(self):
        return f'{self.user.username} Profile'
