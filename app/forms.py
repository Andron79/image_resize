from django import forms
from django.forms import ImageField, URLInput

from .models import Image


class ImageForm(forms.ModelForm):
    class Meta:
        model = Image
        # image_url = forms.URLInput()
        fields = ('image',)
