from django import forms
from django.contrib.auth.forms import UserCreationForm, AuthenticationForm
from django.contrib.auth.models import User
from django.contrib.auth.forms import UsernameField


class RegisterForm(UserCreationForm):
    
    username = forms.CharField(max_length=100, 
                               required=True,
                               widget=forms.TextInput(attrs={"class": "form-control"}))
    
    email = forms.EmailField(max_length=50,
                             required=True,
                             widget=forms.EmailInput(attrs={"class": "form-control"}))
    
    password1 = forms.CharField(max_length=50,
                                required=True,
                                widget=forms.PasswordInput(attrs={"class": "form-control"}))

    password2 = forms.CharField(max_length=50,
                                required=True,
                                widget=forms.PasswordInput(attrs={"class": "form-control"}))

    class Meta:
        model = User
        fields = ["username", "email", "password1", "password2"]
        

class LoginForm(AuthenticationForm):
    
    username = UsernameField(widget=forms.TextInput(attrs={"autofocus": True, "class": "form-control"}))
    password = forms.CharField(
        label="Password",
        strip=False,
        widget=forms.PasswordInput(attrs={"autocomplete": "current-password", "class": "form-control"}),
    )
    
    
    class Meta:
        model = User
        fields = ["username", "password"]