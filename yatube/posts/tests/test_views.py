from http import HTTPStatus

from django.core.cache import cache
from django.test import Client, TestCase
from django.urls import reverse

from ..models import Group, Post, User


class PostViewsTest(TestCase):
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
            text="test-post-text",
        )

    def setUp(self):
        cache.clear()
        self.guest_client = Client()
        self.user = User.objects.create_user(username="StasBasov")
        self.authorized_client = Client()
        self.authorized_client.force_login(self.user)

    def test_pages_uses_correct_template(self):
        templates_pages_names = {
            "posts/index.html": reverse("posts:index"),
            "posts/group_list.html": reverse(
                "posts:group_posts", kwargs={"slug": "test-slug"}
            ),
            "posts/post_detail.html": reverse(
                "posts:post_detail", kwargs={"post_id": self.post.id}
            ),
        }
        for template, reverse_name in templates_pages_names.items():
            with self.subTest(reverse_name=reverse_name):
                response = self.guest_client.get(reverse_name)
                self.assertTemplateUsed(response, template)

    def test_pages_authorized_client_correct_template(self):
        templates_pages_names = {
            "posts/create_post.html": reverse("posts:post_create"),
            "posts/profile.html": reverse(
                "posts:profile", kwargs={"username": self.user.username}
            ),
        }
        for template, reverse_name in templates_pages_names.items():
            with self.subTest(reverse_name=reverse_name):
                response = self.authorized_client.get(reverse_name)
                self.assertTemplateUsed(response, template)

    def test_create_post_author_correct_template(self):
        self.user_2 = User.objects.create_user(username="author")
        self.author = Client()
        self.author.force_login(self.user_2)
        Post.objects.create(
            text="Новый пост", author=self.user_2, id="2", group=self.group
        )
        response = self.author.get(reverse("posts:edit_post", kwargs={"post_id": "2"}))
        self.assertTemplateUsed(response, "posts/create_post.html")

    def test_create_post(self):
        posts_count = Post.objects.count()
        form_data = {
            "text": "test-text",
        }
        response = self.authorized_client.post(
            reverse("posts:post_create"), data=form_data, follow=True
        )
        self.assertRedirects(
            response,
            reverse("posts:profile", kwargs={"username": "StasBasov"}),
        )
        self.assertEqual(Post.objects.count(), posts_count + 1)
        self.assertTrue(
            Post.objects.filter(
                text="test-text",
            ).exists()
        )
        self.assertEqual(response.status_code, HTTPStatus.OK)

    def test_edit_post(self):
        self.user_2 = User.objects.create_user(username="author")
        self.author = Client()
        self.author.force_login(self.user_2)
        Post.objects.create(text="test-text", author=self.user_2, id="2")
        posts_count = Post.objects.count()
        form_data = {
            "text": "test-text",
        }
        response = self.author.post(
            reverse("posts:edit_post", args=("2",)), data=form_data, follow=True
        )
        self.assertRedirects(
            response,
            reverse("posts:post_detail", kwargs={"post_id": "2"}),
        )
        self.assertEqual(Post.objects.count(), posts_count)
        self.assertTrue(
            Post.objects.filter(
                text="test-text",
            ).exists()
        )
        self.assertEqual(response.status_code, HTTPStatus.OK)

    def test_index_show_correct_context(self):
        response = self.guest_client.get(reverse("posts:index"))
        first_object = response.context["page_obj"][0]
        post_text_0 = first_object.text
        self.assertEqual(post_text_0, self.post.text)

    def test_group_posts_filter_by_group(self):
        form_fields = {
            reverse(
                "posts:group_posts", kwargs={"slug": self.group.slug}
            ): Post.objects.filter(group=self.post.group),
        }
        for value, expected in form_fields.items():
            with self.subTest(value=value):
                response = self.guest_client.get(value)
                form_field = response.context["page_obj"]
                self.assertNotIn(expected, form_field)
        response = self.client.get(
            reverse("posts:group_posts", kwargs={"slug": self.group.slug})
        )
        self.assertEqual(len(response.context["posts"]), 1)

    def test_profile_filter_by_auth(self):
        form_fields = {
            reverse("posts:profile", kwargs={"username": "auth"}): Post.objects.filter(
                author=self.post.author
            ),
        }
        for value, expected in form_fields.items():
            with self.subTest(value=value):
                response = self.guest_client.get(value)
                form_field = response.context["page_obj"]
                self.assertNotIn(expected, form_field)
        response = self.client.get(
            reverse("posts:profile", kwargs={"username": "auth"})
        )
        self.assertEqual(len(response.context["posts"]), 1)

    def test_post_detail_one_post_filter_by_id(self):
        response = self.guest_client.get(
            reverse("posts:post_detail", kwargs={"post_id": self.post.id})
        )
        fields = {
            response.context["post"]: Post.objects.get(id=self.post.id),
        }
        for value, expected in fields.items():
            with self.subTest(value=value):
                self.assertEqual(value, expected)

    def test_show_post_in_group(self):
        self.user_2 = User.objects.create_user(username="author")
        self.author = Client()
        self.author.force_login(self.user_2)
        Post.objects.create(
            text="Новый пост", author=self.user_2, id="2", group=self.group
        )
        response = self.guest_client.get(
            reverse("posts:group_posts", kwargs={"slug": "test-slug"})
        )
        first_object = response.context["posts"][0]
        text = first_object.text
        self.assertEqual(text, first_object.text)

    def test_show_post_in_profile(self):
        self.user_2 = User.objects.create_user(username="author")
        self.author = Client()
        self.author.force_login(self.user_2)
        Post.objects.create(
            text="Новый пост", author=self.user_2, id="2", group=self.group
        )
        response = self.guest_client.get(
            reverse("posts:profile", kwargs={"username": "author"})
        )
        first_object = response.context["page_obj"][0]
        text = first_object.text
        self.assertEqual(text, first_object.text)

    def test_check_group_mistake(self):
        form_fields = {
            reverse(
                "posts:group_posts", kwargs={"slug": self.group.slug}
            ): Post.objects.exclude(group=self.post.group),
        }
        for value, expected in form_fields.items():
            with self.subTest(value=value):
                response = self.authorized_client.get(value)
                form_field = response.context["page_obj"]
                self.assertNotIn(expected, form_field)


class PostPaginationTests(TestCase):
    @classmethod
    def setUpClass(cls):
        super().setUpClass()
        cls.user = User.objects.create_user(username="auth")
        cls.some_group = Group.objects.create(
            title="Тестовая группа",
            slug="some_group",
            description="Здесь должны правильно отобразиться записи",
        )

        cls.post_list = []
        for i in range(0, 11):
            cls.post_list.append(
                Post(text=f"Тестовый текст-{i}", group=cls.some_group, author=cls.user)
            )
        Post.objects.bulk_create(cls.post_list)

    def setUp(self):
        self.authorized_client = Client()
        self.authorized_client.force_login(self.user)

    def test_index_firsp_page_posts_count(self):
        cache.clear()
        response = self.client.get(reverse("posts:index"))
        self.assertEqual(len(response.context["page_obj"]), 10)

    def test_second_page_posts_count_index(self):
        response = self.client.get(reverse("posts:index") + "?page=2")
        self.assertEqual(len(response.context["page_obj"]), 1)

    def test_group_list_first_page_count(self):
        response = self.client.get(
            reverse("posts:group_posts", kwargs={"slug": "some_group"})
        )
        self.assertEqual(len(response.context["page_obj"]), 10)

    def test_second_page_posts_count(self):
        response = self.client.get(
            reverse("posts:group_posts", kwargs={"slug": "some_group"}) + "?page=2"
        )
        self.assertEqual(len(response.context["page_obj"]), 1)

    def test_profile_first_page_records(self):
        response = self.client.get(
            reverse("posts:profile", kwargs={"username": "auth"})
        )
        self.assertEqual(len(response.context["page_obj"]), 10)

    def test_second_page_contains_three_records(self):
        response = self.client.get(
            reverse("posts:profile", kwargs={"username": "auth"}) + "?page=2"
        )
        self.assertEqual(len(response.context["page_obj"]), 1)
