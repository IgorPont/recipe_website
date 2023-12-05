from django.db import models
from django.contrib.auth.models import User
from django.utils import timezone
from PIL import Image


def user_directory_path(instance, filename):
    # путь, куда будет осуществлена загрузка MEDIA_ROOT/profile_pics/user_<id>/<filename>
    return 'profile_pics/user_{0}/{1}'.format(instance.user.id, filename)


class Profile(models.Model):
    user = models.OneToOneField(User, on_delete=models.CASCADE, verbose_name="Пользователь сайта")
    image = models.ImageField(default='default.jpg', upload_to=user_directory_path, verbose_name="Аватар")

    def __str__(self):
        return f'{self.user.username} Profile'

    # Автоматическое сжатие загруженных пользователем аватарок
    def save(self):
        super().save()

        img = Image.open(self.image.path)

        if img.height > 300 or img.width > 300:
            output_size = (300, 300)
            img.thumbnail(output_size)
            img.save(self.image.path)
