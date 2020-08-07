from django.http import HttpResponseRedirect
from django.shortcuts import render
from django.urls import reverse_lazy, reverse
from django.views.generic import ListView, CreateView, UpdateView, DetailView, FormView
# from PIL import Image

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
    # fields = ['image']
    # success_url = reverse_lazy('image_resize')


class ImageResize(FormView, UpdateView):
    template_name = 'image.html'
    model = Image
    form_class = ResizeForm

    def post(self, request, *args, **kwargs):
        print(request.POST)
        form = self.form_class(request.POST)
        if form.is_valid():
            from PIL import Image as Img
            print("Форма валидна")
            new_image = Image.objects.get(id=self.kwargs['pk'])
            new_width, new_height = form.cleaned_data['width'], form.cleaned_data['height']
            resize_img = Img.open(new_image.original)
            resize = resize_img.resize((new_width, new_height), Img.ANTIALIAS)
            # form.save()
            resize.show()
            return HttpResponseRedirect('')
