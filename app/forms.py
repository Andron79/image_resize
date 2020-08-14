from os import path
from urllib.parse import urlparse
import requests
from PIL import Image as Img
from django import forms
from django.conf import settings
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
        if (not cleaned_data.get('original')) and (not cleaned_data['image_url']):
            raise forms.ValidationError('Заполните хотя бы одно поле ввода!')
        if cleaned_data['image_url']:  # валидация и загрузка картинки по URL, сохранение на диск
            try:
                resp = requests.get(cleaned_data['image_url'], stream=True).raw
            except requests.exceptions.RequestException as e:
                raise forms.ValidationError('Неправильная ссылка!')
            try:
                img = Img.open(resp)
            except IOError:
                raise forms.ValidationError('Невозможно открыть файл картинки!')
            file_name = (urlparse(cleaned_data['image_url']).path.split('/')[-1]).lower()
            # print(file_name)

            path_original = path.join(settings.MEDIA_URL, 'original', file_name).lower()
            # img.save(path_original, 'jpeg')


            # photo = Image()  # set any other fields, but don't commit to DB (ie. don't save())
            # #name = urlparse(img_url).path.split('/')[-1]
            # image_url = cleaned_data['image_url']
            # # content = urllib3.urlretrieve(image_url)
            # # content = urllib3.urlopen(url).read()
            # content = request.urlopen(image_url)
            # print(content[0])
            #
            #     # See also: http://docs.djangoproject.com/en/dev/ref/files/file/
            # photo.original.save(file_name, File(open(content)), save=True)

            # file_buffer = BytesIO()
            # cleaned_data['original'].save(file_buffer, 'jpeg')

            # cleaned_data['resize'] = path.join(settings.MEDIA_URL, 'resize', 'resize_' + file_name)  # settings.MEDIA_URL,
            # print(cleaned_data['resize'])
            # Image.objects.create(original=cleaned_data['original'])
            # img.save(path_original, 'jpeg')
            # img.save(cleaned_data['resize'], 'jpeg')

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
