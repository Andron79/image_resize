from django.test import TestCase
from app.forms import ImageUploadForm
from app.models import Image


class ImageUploadFormTest(TestCase):

    def setUp(self):
        self.image_url = Image.image_url

    def test_valid_data(self):  # тест сохранения формы
        form = ImageUploadForm({
            'image_url': "https://luxtort.ru/components/com_jshopping/files/img_products/full_114478.jpg",
        })
        self.assertTrue(form.is_valid())
        image = form.save()
        self.assertEqual(image.image_url,
                         "https://luxtort.ru/components/com_jshopping/files/img_products/full_114478.jpg")

    def test_blank_data(self):  # тест на 2 пустых поля ввода
        form = ImageUploadForm({})
        self.assertFalse(form.is_valid())
        self.assertTrue(form.errors, {
            'image_url': ['required'],
            'original': ['required'],
        })

    def test_all_data(self):  # тест на 2 одновременно заполненных поля ввода
        form = ImageUploadForm({
            'image_url': "https://luxtort.ru/components/com_jshopping/files/img_products/full_114478.jpg",
            'original': "23451151.jpg"
        })
        self.assertTrue(form.is_valid())
        self.assertFalse(form.errors, {
            'image_url': ['required'],
            'original': ['required'],
        })

    def test_wrong_urls(self):  # тест с плохой ссылкой
        form = ImageUploadForm({
            'image_url': "https://luxtort.ru/components/com_jshopping/files/img_products/11478.jpg",  # <-- wrong url
        })
        self.assertFalse(form.is_valid())
        self.assertTrue(form.errors, {
            'image_url': ['required'],
        })


class ImageResizeFormTest(TestCase):
    def setUp(self):
        self.height = Image.height
        self.width = Image.width

    def test_blank_data(self):  # тест на 2 пустых поля ввода размеров ресайза
        form = ImageUploadForm({})
        self.assertFalse(form.is_valid())
        self.assertTrue(form.errors, {
            'height': ['required'],
            'width': ['required'],
        })
