import shutil
import tempfile
from http import HTTPStatus

from django import forms
from django.conf import settings
from django.test import Client, TestCase
from django.urls import reverse

from ..models import Group, Post, User

TEMP_MEDIA_ROOT = tempfile.mkdtemp(dir=settings.BASE_DIR)


class PostCreateForm(TestCase):
    @classmethod
    def setUpClass(cls):
        super().setUpClass()
        cls.user = User.objects.create_user(username="auth")
        cls.group = Group.objects.create(
            title="test-title",
            slug="test-slug",
            description="test-description",
        )
        cls.post = Post.objects.create(
            author=cls.user,
            text="test-text",
        )

    def setUp(self):
        self.guest_client = Client()
        self.user = User.objects.create_user(username="StasBasov")
        self.authorized_client = Client()
        self.authorized_client.force_login(self.user)

    class Meta:
        model = Post
        fields = "__all__"

    @classmethod
    def tearDownClass(cls):
        super().tearDownClass()
        shutil.rmtree(TEMP_MEDIA_ROOT, ignore_errors=True)

    def test_post_creation_form(self):
        response = self.authorized_client.get(reverse("posts:post_create"))
        form_fields = {
            "text": forms.fields.CharField, "group": forms.ModelChoiceField}
        for value, expected in form_fields.items():
            with self.subTest(value=value):
                form_field = response.context.get("form").fields.get(value)
                self.assertIsInstance(form_field, expected)
                self.assertEqual(response.status_code, HTTPStatus.OK)

    def test_edit_post_filtered_by_id(self):
        self.user_2 = User.objects.create_user(username="author")
        self.author = Client()
        self.author.force_login(self.user_2)
        Post.objects.create(text="Новый пост", author=self.user_2, id="2")
        response = self.author.get(reverse("posts:edit_post", kwargs={
            "post_id": "2"}))
        fields = {
            "text": forms.fields.CharField, "group": forms.ModelChoiceField}
        for value, expected in fields.items():
            with self.subTest(value=value):
                form_field = response.context.get("form").fields.get(value)
                self.assertIsInstance(form_field, expected)
                self.assertEqual(response.status_code, HTTPStatus.OK)

    def test_an_unauthorized_user_cannot_create_post(self):
        response = self.guest_client.get(reverse("posts:post_create"))
        self.assertRedirects(response, f'{reverse("users:login")}?next={reverse("posts:post_create")}')
        self.assertEqual(response.status_code, HTTPStatus.FOUND)

    def test_an_unauthorized_user_cannot_edit_post(self):
        response = self.guest_client.get(
            reverse("posts:edit_post", kwargs={"post_id": self.post.id})
        )
        self.assertRedirects(response, f'{reverse("users:login")}?next={reverse("posts:edit_post", args=[self.post.id])}')

        self.assertEqual(response.status_code, HTTPStatus.FOUND)
