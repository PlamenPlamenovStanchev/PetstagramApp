from django.contrib.auth.models import User
from django.test import TestCase
from django.urls import reverse

from photos.models import Photo


class TestPhotoDeleteView(TestCase):
    def setUp(self):
        self.credentials_author = {
            'email': 'myemail@mail.com',
            'password': 'parolka-12345'
        }
        self.credentials_visitor = {
            'email': 'myemail2@mail.com',
            'password': 'parolka-12345'
        }

        self.user_author = User.objects.create_user(**self.credentials_author)
        self.user_visitor = User.objects.create_user(**self.credentials_visitor)

        self.photo = Photo.objects.create(
            photo='photo.jpg',
            description='Some test description',
            location='test',
            user=self.user_author,
        )

        self.client.login(**self.credentials_author)

    def test_delete_photo_as_author_expect_success(self):
        response = self.client.post(
            path=reverse('delete_photo', kwargs={'pk': self.photo.pk}),
        )

        self.assertFalse(Photo.objects.filter(pk=self.photo.pk).exists())
        self.assertRedirects(response,reverse('home'))

    def test_delete_photo_as_visitor_expect_http_forbidden_message(self):
        self.client.login(**self.credentials_visitor)

        response = self.client.post(
            path=reverse('delete_photo', kwargs={'pk': self.photo.pk}),
        )

        self.assertTrue(Photo.objects.filter(pk=self.photo.pk).exists())
        self.assertEqual(response.status_code, 403)