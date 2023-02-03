from http import HTTPStatus

from django.test import Client, TestCase
from django.urls import reverse

from ..models import Group, Post, User


class PostUrlsTest(TestCase):
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
            text="text",
        )

    def setUp(self):
        self.guest_client = Client()
        self.user = User.objects.create_user(username="HasNoName")
        self.authorized_client = Client()
        self.authorized_client.force_login(self.user)

    def test_404(self):
        response = self.guest_client.get(
            reverse("posts:group_posts", kwargs={"slug": "404"})
        )
        self.assertTemplateUsed(response, "core/404.html")

    def test_guest_client_unexisting_template(self):
        response = self.guest_client.get("/unexisting_page/")
        self.assertEqual(response.status_code, HTTPStatus.NOT_FOUND)

    def test_create_authorized_client_correct_template(self):
        response = self.authorized_client.get(reverse("posts:post_create"))
        self.assertTemplateUsed(response, "posts/create_post.html")
        response = self.authorized_client.get(
            reverse("posts:profile", kwargs={"username": self.user})
        )
        self.assertTemplateUsed(response, "posts/profile.html")

    def test_create_author_correct_template(self):
        self.user_2 = User.objects.create_user(username="author")
        self.author = Client()
        self.author.force_login(self.user_2)
        Post.objects.create(text="Новый пост", author=self.user_2, id="2")
        response = self.author.get(reverse("posts:edit_post", args=("2",)))
        self.assertEqual(response.status_code, HTTPStatus.OK)

    def test_urls_guest_client_correct_template(self):
        templates_url_names = {
            "posts/index.html": reverse("posts:index"),
            "posts/group_list.html": reverse(
                "posts:group_posts", kwargs={"slug": "test-slug"}
            ),
            "posts/post_detail.html": reverse(
                "posts:post_detail", kwargs={"post_id": self.post.id}
            ),
        }
        for template, url in templates_url_names.items():
            with self.subTest(url=url):
                response = self.guest_client.get(url)
                self.assertTemplateUsed(response, template)

    def test_an_unauthorized_user_cannot_create_post(self):
        response = self.guest_client.get(reverse("posts:post_create"))
        self.assertRedirects(response, "/auth/login/?next=/create/")
        self.assertEqual(response.status_code, 302)

    def test_an_unauthorized_user_cannot_edit_post(self):
        response = self.guest_client.get(
            reverse("posts:edit_post", kwargs={"post_id": "2"})
        )
        self.assertRedirects(response, f"/auth/login/?next=/posts/{2}/edit/")
        self.assertEqual(response.status_code, 302)
