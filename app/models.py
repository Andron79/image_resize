from django.db import models
from django.urls import reverse


class Image(models.Model):
    original = models.ImageField(upload_to='original', blank=True, verbose_name='Файл')
    image_url = models.URLField(null=True, blank=True, verbose_name='Ссылка')
    resize = models.ImageField(upload_to='resize', blank=True, verbose_name='Отредактированное изображение')
    height = models.PositiveSmallIntegerField(blank=True, null=True, verbose_name='Высота')
    width = models.PositiveSmallIntegerField(blank=True, null=True, verbose_name='Ширина')

    def get_absolute_url(self):
        return reverse('image_detail', args=[str(self.pk)])
