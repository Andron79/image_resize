from django.shortcuts import render
from django.urls import reverse_lazy
from django.views.generic import ListView, CreateView

from app.forms import ImageForm
from app.models import Image


class ImageList(ListView):
    Model = Image
    queryset = Image.objects.all()
    template_name = 'index.html'


class ImageUpload(CreateView):
    template_name = 'upload.html'
    model = Image
    form_class = ImageForm
    success_url = reverse_lazy('index')
