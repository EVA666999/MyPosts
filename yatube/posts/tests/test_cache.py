from django.core.cache import cache
from django.test import Client, TestCase
from django.urls import reverse

from ..models import Post, User


class PostViewsTest(TestCase):
    @classmethod
    def setUpClass(cls):
        super().setUpClass()
        cls.user = User.objects.create_user(username="auth")

    def setUp(self):
        self.authorized_client = Client()
        self.authorized_client.force_login(self.user)

    def test_cache_index(self):
        """Проверка хранения и очищения кэша для index."""
        response = self.authorized_client.get(reverse("posts:index"))
        posts = response.content
        Post.objects.create(
            text="test_cache",
            author=self.user,
        )
        response_old = self.authorized_client.get(reverse("posts:index"))
        old_posts = response_old.content
        self.assertEqual(old_posts, posts)
        cache.clear()
        response_new = self.authorized_client.get(reverse("posts:index"))
        new_posts = response_new.content
        self.assertNotEqual(old_posts, new_posts)
