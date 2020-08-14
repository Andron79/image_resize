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
            new_image = Image.objects.get(id=self.kwargs['pk'])
            # print(new_image.resize.url)
            images_resize(new_image.original, form.cleaned_data['height'], form.cleaned_data['width'])
            return HttpResponseRedirect('')
        else:
            form = self.form_class(request.POST or None, request.FILES or None)
            print(request.POST or None, request.FILES or None)
            image = Image.objects.get(id=self.kwargs['pk'])
            return render(request, 'image.html', {'form': form,
                                                  'image': image
                                                  }
                          )
