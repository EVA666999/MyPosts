from django.contrib.auth.decorators import login_required
from django.core.paginator import Paginator
from django.shortcuts import get_object_or_404, redirect, render
from .forms import CommentForm, PostForm
from .models import Comment, Follow, Group, Post, User
from .utils import get_page_context
from django.urls import reverse
from django.http import HttpResponseRedirect
from django.http import JsonResponse
from django.db.models import Count
from django.views.decorators.http import require_POST

SECONDS_CACHE = 20


def index(request):
    posts = Post.objects.all()
    for post in posts:
        post.total_likes = post.total_like()
        post.total_dislikes = post.total_dislike()
    context = get_page_context(posts, request)
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
    context = {"posts": posts, "author": user, "following": following, }
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
    if user != author:
        Follow.objects.get_or_create(user=user, author=author)
    return redirect(reverse('posts:profile', args=[username]))


@login_required
def profile_unfollow(request, username):
    author = get_object_or_404(User, username=username)
    Follow.objects.filter(user=request.user, author=author).delete()
    return redirect('posts:profile', username=author)


def LikeView(request, pk):
    post = get_object_or_404(Post, pk=pk)
    if request.method == 'POST' and request.is_ajax():
        post.like.add(request.user)
    total_likes = post.like.count()
    newCount = None
    if request.user.is_authenticated:
        newCount = total_likes
    data = {
        "total_likes": newCount,
    }
    return JsonResponse(data)


def DisLikeView(request, pk):
    post = get_object_or_404(Post, pk=pk)
    if request.method == 'POST' and request.is_ajax():
        post.dislike.add(request.user)
    total_dislikes = post.dislike.count()
    newCount = None
    if request.user.is_authenticated:
        newCount = total_dislikes
    data = {
        "total_dislikes": newCount,
    }
    return JsonResponse(data)