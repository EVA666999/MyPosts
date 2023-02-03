from django.test import Client, TestCase
from django.urls import reverse

from ..models import Follow, Post, User


class Followtests(TestCase):
    @classmethod
    def setUpClass(cls):
        super().setUpClass()
        cls.author = User.objects.create_user(username="author")
        cls.user = User.objects.create_user(username="StasBasov")
        cls.user1 = User.objects.create_user(username="NotFollower")
        cls.post = Post.objects.create(
            text="Тестовый текст",
            author=cls.author,
        )

    def setUp(self):
        self.guest_client = Client()
        self.authorized_client = Client()
        self.authorized_client.force_login(self.user)
        self.not_follower = Client()
        self.not_follower.force_login(self.user1)

    def test_authorized_user_can_follow(self):
        response = self.authorized_client.get(
            reverse("posts:profile_follow", kwargs={
                "username": self.author.username
            })
        )
        followers = Follow.objects.count()
        self.assertEqual(Follow.objects.count(), followers)
        self.assertTemplateUsed(response, "posts/follow.html")
        print(followers)

    def test_authorized_user_can_unfollow(self):
        response = self.authorized_client.get(
            reverse("posts:profile_unfollow", kwargs={
                "username": self.author.username})
        )
        followers_count = Follow.objects.count()
        print(followers_count)
        self.assertEqual(Follow.objects.count(), followers_count)
        self.assertTemplateUsed(response, "posts/follow.html")

    def test_index_show_correct_context(self):
        Follow.objects.create(user=self.user, author=self.author)
        Follow.objects.filter(user=self.user).exists()
        followers = Follow.objects.count()
        self.assertEqual(Follow.objects.count(), followers)
        print(followers)
        response = self.authorized_client.get(reverse("posts:follow_index"))
        first_object = response.context["page_obj"][0]
        text = first_object.text
        print(text)
        self.assertEqual(text, first_object.text)

    def context_for_non_subscribed_users(self):
        response = self.not_follower.get(reverse("posts:follow_index"))
        first_object = response.context["page_obj"][0]
        text = first_object.text
        self.assertNotIn(text, first_object.text)
