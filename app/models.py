from django.db import models


class Image(models.Model):
    # name = models.CharField(max_length=255, blank=False, verbose_name='Имя')
    image = models.ImageField(upload_to='app', blank=True)
    # image_url = models.ImageField(upload_to='app', blank=True)
    resize_image = models.ImageField(upload_to='app/resize', blank=True)

    # def __str__(self):
    #     return self.image
