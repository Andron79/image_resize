from django.conf.urls.static import static
from django.contrib import admin
from django.urls import path
from app.views import ImageList, ImageUpload, ImageResize
from test_images import settings

urlpatterns = [
    path('admin/', admin.site.urls),
    path('', ImageList.as_view(), name='index'),
    path('upload/', ImageUpload.as_view(), name='upload_image'),
    path('image/<int:pk>', ImageResize.as_view(), name='image_detail'),
]

if settings.DEBUG:
    urlpatterns += static(settings.MEDIA_URL, document_root=settings.MEDIA_ROOT)


