"""from django.contrib.auth import get_user_model
from django.test import Client, TestCase
from django.urls import reverse

User = get_user_model()


class SignUpUserTests(TestCase):
    def setUp(cls) -> None:
        cls.guest_client = Client()

    def test_signup(self):
        user_count = User.objects.count()
        form_data = {
            'first_name': 'Testsignupp',
            'last_name': 'Testlastnamee',
            'email': 'teestemail134fsa@gmail.com',
            'username': 'Userforsignupp',
            'password1': 'Kohkay1193122',
            'password2': 'Kohkay1193122'
        }
        response = self.guest_client.post(
            reverse('users:signup'),
            data=form_data,
            follow=True
        )
        self.assertRedirects(response, reverse('posts:index'))
        self.assertEqual(User.objects.count(), user_count + 1)
        self.assertTrue(
            User.objects.filter(
                first_name='Testsignupp',
                last_name='Testlastnamee',
                email='teestemail134fsa@gmail.com',
                username='Userforsignupp',
            )
            .exists()
        )
        self.assertEqual(response.status_code, 200)"""
