from django.db import models
from django.urls import reverse


class Image(models.Model):
    image = models.ImageField(upload_to='original', blank=True, verbose_name='Загрузка с компьютера')
    # image_url = models.ImageField(upload_to='original', blank=True, verbose_name='URL изображения')
    resize_image = models.ImageField(upload_to='resize', blank=True, verbose_name='Отредактированное изображение')

    def get_absolute_url(self):
        return reverse('image_detail', args=[str(self.pk)])
