from django import forms
from django.contrib.auth.forms import UserCreationForm
from django.contrib.auth.models import User


class RequestForm(forms.Form):
    user_input = forms.CharField(label="Что вы хотите изучить?", max_length=100)


class SignUpForm(UserCreationForm):
    email = forms.EmailField(required=True)
    first_name = forms.CharField(max_length=100)
    last_name = forms.CharField(max_length=100)
    city = forms.CharField(max_length=100)

    class Meta:
        model = User
        fields = [
            "username",
            "email",
            "first_name",
            "last_name",
            "city",
            "password1",
            "password2",
        ]