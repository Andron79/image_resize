from django import forms
from django.forms import ImageField, URLInput

from .models import Image


class ImageUploadForm(forms.ModelForm):
    class Meta:
        model = Image
        # image_url = forms.URLInput()
        fields = ('image',)


class ResizeForm(forms.ModelForm):
    height = forms.IntegerField()
    width = forms.IntegerField()

    class Meta:
        model = Image
        fields = ('height', 'width',)
