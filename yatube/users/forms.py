from django import forms
from django.contrib.auth import get_user_model
from django.contrib.auth.forms import UserCreationForm

from .models import Contact

User = get_user_model()


class UserRegistrationForm(UserCreationForm):
    first_name = forms.CharField(widget=forms.TextInput(attrs={
     'class': 'form-control py-4', 'placeholder': 'Введите имя',
    }))
    last_name = forms.CharField(widget=forms.TextInput(attrs={
     'class': 'form-control py-4', 'placeholder': 'Введите фамилию',
    }))
    username = forms.CharField(widget=forms.TextInput(attrs={
     'class': 'form-control py-4', 'placeholder': 'Введите имя пользователя',
    }))
    email = forms.CharField(widget=forms.EmailInput(attrs={
     'class': 'form-control py-4', 'placeholder': 'Введите емаил',
    }))
    password1 = forms.CharField(
        label='Password', widget=forms.PasswordInput(attrs={'class': 'form-control'})
    )
    password2 = forms.CharField(
        label='Password confirmation', widget=forms.PasswordInput(attrs={'class': 'form-control'})
    )
    image = forms.ImageField(widget=forms.FileInput(attrs={
    'class': 'form-control py-4', 'placeholder': 'Выберите аватар',
    }), required=False)

    class Meta:
        model = User
        fields = ('first_name', 'last_name', 'username', 'email', 'password1', 'password2', 'image',)


class ContactForm(forms.ModelForm):
    class Meta:
        model = Contact
        fields = ("name", "email", "subject", "body")


def clean_subject(self):
    data = self.cleaned_data["subject"]

    if "спасибо" not in data.lower():
        raise forms.ValidationError("Вы обязательно должны нас поблагодарить!")

    return data


class UserUpdateForm(forms.ModelForm):
    email = forms.EmailField()

    class Meta:
        model = get_user_model()
        fields = ["first_name", "last_name", "email"]
