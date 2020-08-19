from urllib.parse import urlparse
import requests
from PIL import Image as Img
from django import forms
from urllib import request
from django.core.files.base import ContentFile
from .models import Image


class ImageUploadForm(forms.ModelForm):
    """
    Валидации по условиям задания и сохранение полученного по ссылке файла
    """

    class Meta:
        model = Image
        fields = ('image_url', 'original',)

    def clean(self):
        cleaned_data = self.cleaned_data
        if cleaned_data['image_url'] and cleaned_data['original']:
            raise forms.ValidationError('Заполните только одно поле ввода!')
        if cleaned_data.get('original') is None and cleaned_data['image_url'] is None:
            raise forms.ValidationError('Заполните хотя бы одно поле ввода!')
        if cleaned_data['image_url']:  # валидация и загрузка картинки по URL
            try:
                resp = requests.get(cleaned_data['image_url'], stream=True).raw
            except requests.exceptions.RequestException as e:
                raise forms.ValidationError('Неправильная ссылка!')
            try:
                img = Img.open(resp)
            except IOError:
                raise forms.ValidationError('Невозможно открыть файл картинки!')
        return cleaned_data

    def save(self, force_insert=False, force_update=False, commit=True):
        cleaned_data = self.cleaned_data
        original = super(ImageUploadForm, self).save(commit=False)
        if cleaned_data['image_url']:
            image_url = self.cleaned_data['image_url']
            image_name = urlparse(cleaned_data['image_url']).path.split('/')[-1].lower()
            response = request.urlopen(image_url)
            original.original.save(image_name, ContentFile(response.read()), save=False)
        if commit:
            original.save()
        return original


class ResizeForm(forms.ModelForm):
    class Meta:
        model = Image
        fields = ('height', 'width',)

    def clean(self):
        cleaned_data = self.cleaned_data
        if cleaned_data['height'] is None and cleaned_data['width'] is None:  # Если не задано параметров
            raise forms.ValidationError('Небходимо заполнить хотя бы одно поле ввода!')
