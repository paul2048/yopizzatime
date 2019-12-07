from django.contrib.auth.models import User
from django import forms

class LoginForm(forms.Form):
    email = forms.CharField(label="Email", max_length=64, widget=forms.EmailInput(attrs={"data-label": "Email*"}))
    password = forms.CharField(label="Password", max_length=64, widget=forms.PasswordInput(attrs={"data-label": "Password*"}))    

class RegisterForm(forms.Form):
    username = forms.CharField(label="Username", max_length=64, widget=forms.TextInput(attrs={"data-label": "Username*"}))
    email = forms.CharField(label="Email", max_length=64, widget=forms.EmailInput(attrs={"data-label": "Email*"}))
    first_name = forms.CharField(label="First Name", max_length=64, widget=forms.TextInput(attrs={"data-label": "First Name*"}))
    last_name = forms.CharField(label="Last Name", max_length=64, widget=forms.TextInput(attrs={"data-label": "Last Name*"}))
    password = forms.CharField(label="Password", max_length=64, widget=forms.PasswordInput(attrs={"data-label": "Password*"}))
    confirm = forms.CharField(label="Confirm Password", max_length=64, widget=forms.PasswordInput(attrs={"data-label": "Confirm Password*"}))