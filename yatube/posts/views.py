from django.contrib.auth.decorators import login_required
from django.core.paginator import Paginator
from django.shortcuts import get_object_or_404, redirect, render
from django.views.decorators.cache import cache_page

from .forms import CommentForm, PostForm
from .models import Comment, Follow, Group, Post, User
from .utils import get_page_context

SECONDS_CACHE = 20


@cache_page(SECONDS_CACHE, key_prefix="index_page")
def index(request):
    context = get_page_context(Post.objects.all(), request)
    return render(request, "posts/index.html", context)


def group_posts(request, slug):
    group = get_object_or_404(Group, slug=slug)
    posts = Post.objects.select_related("group").order_by("-pub_date")[:10]
    context = {
        "group": group,
        "posts": posts,
    }
    context.update(get_page_context(group.posts.all(), request))
    return render(request, "posts/group_list.html", context)


def profile(request, username):
    user = get_object_or_404(User, username=username)
    posts = user.posts.select_related("group", "author")
    following = (
        request.user.is_authenticated
        and Follow.objects.filter(
            user=request.user.id,
            author=user,
        ).exists()
    )
    context = {"posts": posts, "author": user, "following": following}
    context.update(get_page_context(posts, request))
    return render(request, "posts/profile.html", context)


def post_detail(request, post_id):
    post = get_object_or_404(Post, pk=post_id)
    form = CommentForm(request.POST or None)
    comments = Comment.objects.filter(post=post)
    context = {"post": post, "form": form, "comments": comments}
    return render(request, "posts/post_detail.html", context)


@login_required
def post_create(request):
    if request.method == "POST":
        form = PostForm(request.POST, files=request.FILES or None)
        if form.is_valid():
            form = form.save(commit=False)
            form.author = request.user
            form.save()
            return redirect("posts:profile", request.user.username)
        return render(request, "posts/create_post.html", {"form": form})
    form = PostForm()
    return render(request, "posts/create_post.html", {"form": form})


@login_required
def post_edit(request, post_id):
    post = get_object_or_404(Post, id=post_id)
    is_edit = True
    form = PostForm(instance=Post.objects.get(pk=post_id))
    if request.method == "POST":
        form = PostForm(
            request.POST, files=request.FILES or None, instance=post)
        if form.is_valid():
            post = form.save(commit=False)
            post.author = request.user
            post.save()
            return redirect("posts:post_detail", post_id=post.id)

    post = get_object_or_404(Post, id=post_id)
    if request.method == "GET":
        if request.user != post.author:
            return redirect("posts:post_detail", post_id=post.id)
        form = PostForm(instance=post)
    context = {"form": form, "is_edit": is_edit}
    return render(request, "posts/create_post.html", context)


@login_required
def add_comment(request, post_id):
    post = get_object_or_404(Post, pk=post_id)
    form = CommentForm(request.POST or None)
    if form.is_valid():
        comment = form.save(commit=False)
        comment.author = request.user
        comment.post = post
        comment.save()
    return redirect("posts:post_detail", post_id=post_id)


@login_required
def follow_index(request):
    user = request.user
    posts = Post.objects.filter(author__following__user=user)
    paginator = Paginator(posts, 10)
    page_number = request.GET.get("page")
    page_obj = paginator.get_page(page_number)
    follower = Follow.objects.filter(user__following__author=user).exists()
    following = False
    if user != follower:
        following = True
    context = {"posts": posts, "page_obj": page_obj, "following": following}
    return render(request, "posts/follow.html", context)


@login_required
def profile_follow(request, username):
    author = get_object_or_404(User, username=username)
    user = request.user
    if (
        user != author
        and not Follow.objects.filter(
            user=request.user, author=author).exists()
    ):
        Follow.objects.get_or_create(user=user, author=author)
    return render(request, "posts/follow.html")


@login_required
def profile_unfollow(request, username):
    author = get_object_or_404(User, username=username)
    follower = Follow.objects.filter(user__following__author=request.user)
    Follow.objects.filter(user=request.user, author=author).delete()
    context = {" follower": follower}
    return render(request, "posts/follow.html", context)
