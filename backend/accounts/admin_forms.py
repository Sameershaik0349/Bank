from django.contrib.auth.forms import AuthenticationForm
from django import forms

class CustomAdminLoginForm(AuthenticationForm):
    """
    Custom Admin Login Form to disable autocomplete and ensure a clean login experience.
    """
    username = forms.CharField(widget=forms.TextInput(attrs={
        'class': 'form-control',
        'placeholder': 'Username',
        'autocomplete': 'off',  # Prevent autofill
        'autofocus': True,
    }))
    password = forms.CharField(widget=forms.PasswordInput(attrs={
        'class': 'form-control',
        'placeholder': 'Password',
        'autocomplete': 'new-password',  # Prevent autofill
    }))
