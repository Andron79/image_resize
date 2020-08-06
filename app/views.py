from django.shortcuts import render
from django.urls import reverse_lazy, reverse
from django.views.generic import ListView, CreateView, UpdateView, DetailView, FormView

from app.forms import ImageUploadForm, ResizeForm
from app.models import Image


class ImageList(ListView):
    Model = Image
    queryset = Image.objects.all()
    template_name = 'index.html'


class ImageUpload(CreateView):
    template_name = 'upload.html'
    model = Image
    form_class = ImageUploadForm
    success_url = reverse_lazy('index')


class ImageResize(FormView, UpdateView):
    template_name = 'image.html'
    model = Image
    # form_class = ResizeForm
    fields = ['image',]
    success_url = reverse_lazy('image_resize')
