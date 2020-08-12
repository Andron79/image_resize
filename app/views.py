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


class ImageUpload(CreateView):  # TODO
    template_name = 'upload.html'
    model = Image
    form_class = ImageUploadForm

    # success_url = reverse_lazy('image_detail')
    # fields = ['image_url', 'original', 'resize']
    # def get_success_url(self):
    #     return reverse('image_detail', kwargs={'pk': self.kwargs['pk']})

    def post(self, request, *args, **kwargs):
        form = self.form_class(request.POST, request.FILES)
        if form.is_valid():
            img_detail = form.save()

            # print(image.image_url, image.original)
            return redirect(img_detail)
            # return HttpResponseRedirect('')
            # return render(request, 'upload.html', {'form': form})
            # return reverse(ImageResize, pk=id)
            # return HttpResponseRedirect(self.get_success_url())
        else:
            form = self.form_class(request.POST, request.FILES)
            # print(request.POST, request.FILES)
            return render(request, 'upload.html', {'form': form})


class ImageResize(FormView, UpdateView):
    template_name = 'image.html'
    model = Image
    form_class = ResizeForm

    def post(self, request, *args, **kwargs):
        form = self.form_class(request.POST)
        if form.is_valid():
            new_image = Image.objects.get(id=self.kwargs['pk'])
            images_resize(new_image.original, form.cleaned_data['height'], form.cleaned_data['width'])
            return HttpResponseRedirect('')
        else:
            form = self.form_class(request.POST)
            # print(request.POST, request.FILES)
            return render(request, 'image.html', {'form': form})
