from django.db import models
from django.contrib.auth.models import User
from django.core.files.storage import default_storage
from PIL import Image


def user_directory_path(instance, filename):
    """
    Генерация пути, куда будет осуществлена загрузка изображения
    (MEDIA_ROOT/users_media/profile_pics/user_<id>/<filename>)
    """
    return 'users_media/profile_pics/user_{0}/{1}'.format(instance.user.id, filename)


class Profile(models.Model):
    user: User = models.OneToOneField(User, on_delete=models.CASCADE, verbose_name="Пользователь сайта")
    image = models.ImageField(default='avatar_default.jpg', upload_to=user_directory_path, verbose_name="Аватар")

    class Meta:
        verbose_name = 'Профиль пользователя сайта'
        verbose_name_plural = 'Профили пользователей сайта'

    def __str__(self):
        return f'{self.user.username} Profile'

    def save(self, *args, **kwargs):
        """
        Переопределение метода save для сжатия загруженных пользователем аватарок,
        а также удаление старых аватарок, при их обновлении новыми
        """
        old_image_path = self.image.path if self.pk else None

        super().save(*args, **kwargs)

        if self.image and old_image_path:
            # Перед сохранением нового изображения удаляем старое
            if default_storage.exists(old_image_path):
                default_storage.delete(old_image_path)

        valid_extensions = ['.jpg', '.jpeg', '.png', '.gif']

        if any(self.image.path.lower().endswith(ext) for ext in valid_extensions):
            # Проверка, что загруженный файл является изображением
            img = Image.open(self.image.path)

            if img.width > 300 or img.height > 300:
                # Сжимаем изображение
                output_size = (300, 300)
                img.thumbnail(output_size)
                img.save(self.image.path)

    def delete(self, *args, **kwargs):
        """
        Переопределение метода delete для удаления изображения при удалении профиля
        """
        self.image.delete()
        super().delete(*args, **kwargs)
