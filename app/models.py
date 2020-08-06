from django.db import models
from django.urls import reverse


class Image(models.Model):
    # name = models.CharField(max_length=255, blank=False, verbose_name='Имя')
    image = models.ImageField(upload_to='app', blank=True, verbose_name='Оригинальное изображение')
    # image_url = models.ImageField(upload_to='app', blank=True)
    resize_image = models.ImageField(upload_to='app/resize', blank=True, verbose_name='Оредактированное изображение')

    # def __str__(self):
    #     return self.image

    def get_absolute_url(self):
        return reverse('image_detail', args=[str(self.id)])
