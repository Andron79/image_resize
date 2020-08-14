from PIL import Image as Img


def images_resize(image, height_res, width_res):
    """Функция ресайза изображения"""
    resize_img = Img.open(image)
    width, height = resize_img.size

    if height_res is None and width_res is None:  # Если нет никаких параметров, оставляем без изменений
        width_res, height_res = width, height

    if height_res and width_res is None:  # ресайз при наличии только высоты
        width_res = int(height_res * width / height)

    elif width_res and height_res is None:  # ресайз при наличии только ширины
        height_res = int(width_res * height / width)

    resize = resize_img.resize((width_res, height_res), Img.ANTIALIAS)
    resize.save('media/resize/1222.png', 'jpeg')
    resize.show()
