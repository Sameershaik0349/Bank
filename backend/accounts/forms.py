from django import forms
from django.contrib.auth.forms import UserCreationForm as BaseUserCreationForm
from .models import User
from django.core.validators import RegexValidator
from django.core.exceptions import ValidationError
import re

class UserCreationForm(BaseUserCreationForm):
    first_name = forms.CharField(
        required=True,
        min_length=2,
        validators=[RegexValidator(r'^[a-zA-Z]+$', 'Only alphabetic characters are allowed.')],
        widget=forms.TextInput(attrs={'placeholder': 'First Name'})
    )
    last_name = forms.CharField(
        required=True,
        min_length=2,
        validators=[RegexValidator(r'^[a-zA-Z]+$', 'Only alphabetic characters are allowed.')],
        widget=forms.TextInput(attrs={'placeholder': 'Last Name'})
    )
    email = forms.EmailField(
        required=True,
        widget=forms.EmailInput(attrs={'placeholder': 'Email Address'})
    )
    
    class Meta(BaseUserCreationForm.Meta):
        model = User
        fields = ('username', 'email', 'first_name', 'last_name', 'phone_number', 'address')

    def clean_username(self):
        username = self.cleaned_data.get('username')
        # Check if username exists (simpler check, letting Django handle other constraints)
        if User.objects.filter(username=username).exists():
             raise ValidationError("A user with that username already exists.")
        return username

    def clean_email(self):
        email = self.cleaned_data.get('email')
        if User.objects.filter(email=email).exists():
            raise ValidationError("A user with this email already exists.")
        return email

    def clean_password1(self):
        password = self.cleaned_data.get('password1')
        if len(password) < 8:
            raise ValidationError("Password must be at least 8 characters long.")
        if not re.search(r'[A-Z]', password):
            raise ValidationError("Password must contain at least one uppercase letter.")
        if not re.search(r'[a-z]', password):
            raise ValidationError("Password must contain at least one lowercase letter.")
        if not re.search(r'[0-9]', password):
            raise ValidationError("Password must contain at least one number.")
        if not re.search(r'[!@#$%^&*(),.?":{}|<>]', password):
            raise ValidationError("Password must contain at least one special character.")
        return password

from django.contrib.auth.forms import AuthenticationForm

class UserLoginForm(AuthenticationForm):
    username = forms.CharField(widget=forms.TextInput(attrs={
        'class': 'form-control',
        'placeholder': 'Username',
        'autocomplete': 'off',
        'autofocus': True,
    }))
    password = forms.CharField(widget=forms.PasswordInput(attrs={
        'class': 'form-control',
        'placeholder': 'Password',
        'autocomplete': 'new-password',
    }))
