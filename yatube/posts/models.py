from django.contrib.auth import get_user_model
from django.contrib.auth.models import User
from django.db import models

from .max_length import MAX_LEGTH

User = get_user_model()


class Post(models.Model):
    dislike = models.ManyToManyField(User, related_name="disliked_posts")
    like = models.ManyToManyField(User, related_name="blog_posts")
    text = models.TextField(
        verbose_name="Текст", help_text="Введите текст поста")
    pub_date = models.DateTimeField(
        auto_now_add=True, verbose_name="Дата публикации")
    author = models.ForeignKey(
        User, on_delete=models.CASCADE,
        related_name="posts", verbose_name="Автор"
    )
    group = models.ForeignKey(
        "Group",
        on_delete=models.SET_NULL,
        blank=True,
        null=True,
        related_name="posts",
        max_length=MAX_LEGTH,
        verbose_name="Группа",
        help_text=("Группа, к которой будет относиться пост"),
    )
    image = models.ImageField("Картинка", upload_to="posts/", blank=True)

    def total_like(self):
        return self.like.count()
    
    def total_dislike(self):
        return self.dislike.count()

    class Meta:
        verbose_name = "Пост"
        verbose_name_plural = "Посты"
        ordering = ("-pub_date",)

    def __str__(self):
        return self.text


class Group(models.Model):
    title = models.CharField(max_length=200, verbose_name="Заголовок")
    slug = models.SlugField(unique=True, verbose_name="Слаг")
    description = models.TextField(
        verbose_name="Описание", help_text="Введите текст поста"
    )

    class Meta:
        verbose_name = "Группа"
        verbose_name_plural = "Группы"

    def __str__(self):
        return self.title


class Contact(models.Model):
    name = models.CharField(max_length=100)


class Comment(models.Model):
    post = models.ForeignKey(
        Post, on_delete=models.CASCADE,
        related_name="comments", verbose_name="Пост"
    )
    author = models.ForeignKey(
        User, on_delete=models.CASCADE,
        related_name="comments", verbose_name="Автор"
    )
    text = models.TextField(
        verbose_name="Текст", help_text="Введите текст комментария")
    created = models.DateTimeField(
        auto_now_add=True, verbose_name="Дата публикации коментария"
    )

    class Meta:
        verbose_name = "Коментарий"
        verbose_name_plural = "Коментарии"

    def __str__(self):
        return self.text


class Follow(models.Model):
    user = models.ForeignKey(
        User,
        on_delete=models.CASCADE,
        related_name="follower",
        verbose_name="Подписчик",
    )
    author = models.ForeignKey(
        User,
        on_delete=models.CASCADE,
        related_name="following",
        verbose_name="Подписан на ",
    )

    class Meta:
        unique_together = (("author", "user"),)
        constraints = [
            models.UniqueConstraint(
                fields=["user", "author"],
                name="unique_follow",
            )
        ]

    def __str__(self):
        return self.user, self.author


class Profile(models.Model):
    user = models.OneToOneField(User, on_delete=models.CASCADE)
    image = models.ImageField(default='default.jpg', upload_to="posts/")

    def __str__(self):
        return self.user