'''from django import forms
from django.contrib.auth import get_user_model
from django.test import Client, TestCase
from django.urls import reverse

from ..models import Contact

User = get_user_model()


class ContactViewsTest(TestCase):
    @classmethod
    def setUpClass(cls):
        super().setUpClass()
        cls.user = User.objects.create_user(username='auth')
        cls.group = Contact.objects.create(
            name='name',
            email='Емаил',
            subject='Субьект',
            body='Тело'
        )

    def setUp(self):
        self.guest_client = Client()
        self.user = User.objects.create_user(username='StasBasov')
        self.authorized_client = Client()
        self.authorized_client.force_login(self.user)

    def test_pages_users_correct_template(self):
        """URL-адрес использует соответствующий шаблон."""
        templates_pages_names = {
            'users/signup.html': reverse('users:signup'),
            'users/logged_out.html': reverse('users:logout'),
            'users/login.html': reverse('users:login'),
        }
        for template, reverse_name in templates_pages_names.items():
            with self.subTest(reverse_name=reverse_name):
                response = self.guest_client.get(reverse_name)
                self.assertTemplateUsed(response, template)

    def test_pages_users_authorized(self):
        """URL-адрес использует соответствующий шаблон."""
        templates_pages_names = {
            'users/password_change_form.html': reverse(
                'users:password_change'),
            'users/password_change_done.html': reverse(
                'users:password_change_done'),
            'users/password_reset_form.html': reverse(
                'users:password_reset'),
            'users/password_reset_done.html': reverse(
                'users:password_reset_done'),
            'users/password_reset_complete.html': reverse(
                'users:password_reset_done1')


        }
        for template, reverse_name in templates_pages_names.items():
            with self.subTest(reverse_name=reverse_name):
                response = self.authorized_client.get(reverse_name)
                self.assertTemplateUsed(response, template)

    def test_users_create_show_correct_context(self):
        response = self.guest_client.get(reverse('users:signup'))
        form_fields = {
            'email': forms.fields.EmailField,
            'first_name': forms.fields.CharField,
            'last_name': forms.fields.CharField,
            'username': forms.fields.CharField
        }
        for value, expected in form_fields.items():
            with self.subTest(value=value):
                form_field = response.context.get('form').fields.get(value)
                # Проверяет, что поле формы является экземпляром
                # указанного класса
                self.assertIsInstance(form_field, expected)'''
