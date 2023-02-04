from http import HTTPStatus

from django.test import Client, TestCase
from django.urls import reverse

from posts.forms import CommentForm

from ..models import Comment, Post, User


class PostCommentstests(TestCase):
    @classmethod
    def setUpClass(cls):
        super().setUpClass()
        cls.user = User.objects.create_user(username="auth")
        cls.post = Post.objects.create(
            text="Тестовый текст",
            author=cls.user,
        )
        cls.form = CommentForm
        cls.comment = Comment.objects.create(
            text="Комент", author=cls.user, post_id="1"
        )
        cls.post = Post.objects.create(
            author=cls.user,
            text="Тестовый коммент",
        )

    def setUp(self):
        self.guest_client = Client()
        self.user = User.objects.create_user(username="StasBasov")
        self.authorized_client = Client()
        self.authorized_client.force_login(self.user)

    def test_create_comment_guest_client(self):
        response = self.guest_client.get(
            reverse("posts:add_comment", kwargs={"post_id": self.post.id})
        )
        self.assertEqual(response.status_code, 302)

    def test_successful_submission_the_comment(self):
        comment_count = Comment.objects.count()
        form_data = {
            "text": "Коммент",
        }
        response = self.authorized_client.post(
            reverse("posts:add_comment", kwargs={"post_id": self.post.id}),
            data=form_data,
            follow=True,
        )
        self.assertRedirects(
            response, reverse("posts:post_detail", kwargs={
                "post_id": self.post.id})
        )
        self.assertEqual(Post.objects.count(), comment_count + 1)
        self.assertTrue(
            Comment.objects.filter(
                text="Коммент",
            ).exists()
        )
        self.assertEqual(response.status_code, HTTPStatus.OK)
