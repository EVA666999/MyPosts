from django.shortcuts import redirect, render, HttpResponseRedirect
from django.urls import reverse_lazy
from django.views.generic import CreateView
from django.views.generic.base import TemplateView
from django.contrib import messages
from django.urls import reverse

from .forms import Contact, ContactForm, UserRegistrationForm


def signup(request):
    if request.method == 'POST':
        form = UserRegistrationForm(request.POST, request.FILES)
        if form.is_valid():
            form.save()
            messages.success(request, 'Поздравляем вы успешно зарегестрировались!')
            return HttpResponseRedirect(reverse('users:login'))
    else:
        form = UserRegistrationForm()
    context = {'form': form}
    return render(request, 'users/signup.html', context)


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
