from django.core.files.uploadedfile import InMemoryUploadedFile
from django.http import HttpResponseRedirect
from django.shortcuts import render, redirect
from django.views.generic import ListView, CreateView, UpdateView, FormView
from app.forms import ImageUploadForm, ResizeForm
from app.models import Image
from app.utilites import images_resize


class ImageList(ListView):
    Model = Image
    queryset = Image.objects.all()
    template_name = 'index.html'


class ImageUpload(CreateView):
    template_name = 'upload.html'
    model = Image
    form_class = ImageUploadForm

    def post(self, request, *args, **kwargs):
        form = self.form_class(request.POST, request.FILES)
        if form.is_valid():
            img_detail = form.save()
            return redirect(img_detail)
        else:
            form = self.form_class(request.POST or None, request.FILES or None)
            return render(request, 'upload.html', {'form': form})


class ImageResize(FormView, UpdateView):
    template_name = 'image.html'
    model = Image
    form_class = ResizeForm

    def post(self, request, *args, **kwargs):
        form = self.form_class(request.POST)
        if form.is_valid():
            cleaned_data = form.cleaned_data
            instance = Image.objects.get(id=self.kwargs['pk'])
            original = getattr(instance, 'original')
            image_name = ('resize_' + (str(original).split('/')[-1])).lower()
            height_res = cleaned_data['height']
            width_res = cleaned_data['width']
            image_res = original
            pillow_image = images_resize(
                image_res,
                height_res,
                width_res
            )
            instance.resize.delete(image_name)
            instance.resize.save(image_name,
                                 InMemoryUploadedFile(
                                     pillow_image,
                                     image_name,
                                     None,
                                     pillow_image.tell,
                                     None,
                                     None
                                 ), save=True)
            return HttpResponseRedirect('')
        else:
            form = self.form_class(request.POST or None, request.FILES or None)
            image = Image.objects.get(id=self.kwargs['pk'])
            return render(request, 'image.html', {'form': form,
                                                  'image': image
                                                  }
                          )
