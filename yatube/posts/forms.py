from django.forms import ModelForm
from django import forms
from .models import Comment, Post
from .models import Profile


class PostForm(ModelForm):
    class Meta:
        model = Post
        fields = ("text", "group", "image")


class CommentForm(ModelForm):
    class Meta:
        model = Comment
        fields = ("text",)


class ProfileUpdateForm(ModelForm):
    class Meta:
        model = Profile
        fields = ['image']