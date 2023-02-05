from django.shortcuts import redirect, render
from django.urls import reverse_lazy
from django.views.generic import CreateView
from django.views.generic.base import TemplateView

from .forms import Contact, ContactForm, CreationForm


class SignUp(CreateView):
    form_class = CreationForm
    success_url = reverse_lazy("posts:index")
    template_name = "users/signup.html"


def only_user_view(request):
    if not request.user.is_authenticated:
        return redirect("/auth/login/")


def authorized_only(func):
    def check_user(request, *args, **kwargs):
        if request.user.is_authenticated:
            return func(request, *args, **kwargs)
        return redirect("/auth/login/")

    return check_user


def user_contact(request):
    contact = Contact.objects.get(pk=3)
    form = ContactForm(instance=contact)
    return render(request, "users/contact.html", {"form": form})


class JustStaticPage(TemplateView):
    template_name = "app_name/just_page.html"


def indexx(request):
    return render(request, "app_name/index.html")
