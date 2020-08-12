from urllib.parse import urlparse
from os import path
import requests
from django import forms
from django.conf import settings
from .models import Image

from django.core.exceptions import ValidationError
from django.forms import ImageField, URLInput
from PIL import Image as Img


class ImageUploadForm(forms.ModelForm):
    """
    Все валидации по условиям задания и сохранение полученного по ссылке файла
    """

    def clean(self): #TODO
        cleaned_data = self.cleaned_data
        if cleaned_data['image_url'] and cleaned_data['original']:
            raise forms.ValidationError('Заполните только одно поле ввода!')
        if (not cleaned_data.get('original')) and (not cleaned_data['image_url']):
            raise forms.ValidationError('Заполните хотя бы одно поле ввода!')
        if cleaned_data['image_url']:  # валидация и загрузка картинки по URL, сохранение на диск 2-х копий картинки
            try:
                resp = requests.get(cleaned_data['image_url'], stream=True).raw
            except requests.exceptions.RequestException as e:
                raise forms.ValidationError('Неправильная ссылка!')
            try:
                img = Img.open(resp)
            except IOError:
                raise forms.ValidationError('Невозможно открыть файл картинки!')
            file_name = urlparse(cleaned_data['image_url']).path.split('/')[-1]
            # print(file_name)
            cleaned_data['original'] = path.join(settings.MEDIA_ROOT, 'original', file_name)
            # print(cleaned_data['original'])
            cleaned_data['resize'] = path.join(settings.MEDIA_ROOT, 'resize', 'resize_' + file_name)
            img.save(cleaned_data['original'])
            img.save(cleaned_data['resize'])

        # if cleaned_data.get('original'):
        #     #file_name = urlparse(cleaned_data['original']).path.split('/')[-1]
        #     file_name = cleaned_data['original']
        #     #cleaned_data['original'] = path.join(settings.MEDIA_ROOT, 'original', file_name)
        #     # cleaned_data['resize'] = path.join(settings.MEDIA_ROOT, 'resize', 'resize_' + file_name)
        #     img = Img.open(cleaned_data['original'])
        #     img.save(cleaned_data['original'])
        #     # img.save(cleaned_data['resize'])


        # print(cleaned_data)
        return cleaned_data

    # def save(self, commit=True):
    #     cleaned_data = self.cleaned_data
    #     pass

    class Meta:
        model = Image
        fields = ('image_url', 'original',)


class ResizeForm(forms.ModelForm):

    class Meta:
        model = Image
        fields = ('height', 'width',)
