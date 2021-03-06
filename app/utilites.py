from io import BytesIO

from PIL import Image as Img
from django.core.files.base import ContentFile


def images_resize(image_res, height_res, width_res):
    """Функция ресайза изображения"""
    resize_img = Img.open(image_res)
    width, height = resize_img.size

    if height_res and width_res is None:  # ресайз при наличии только высоты
        width_res = int(height_res * width / height)

    elif width_res and height_res is None:  # ресайз при наличии только ширины
        height_res = int(width_res * height / width)

    resize = resize_img.resize((width_res, height_res), Img.ANTIALIAS)
    buffer = BytesIO()
    resize.save(fp=buffer, format='JPEG')
    return ContentFile(buffer.getvalue())
