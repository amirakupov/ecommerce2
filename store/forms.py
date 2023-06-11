from django import forms
from django.contrib.auth.forms import UserCreationForm, AuthenticationForm
from .models import Customer

class LoginForm(forms.Form):
    username = forms.CharField()
    password = forms.CharField(widget=forms.PasswordInput)
