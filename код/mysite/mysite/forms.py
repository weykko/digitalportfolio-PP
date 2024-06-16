from django.forms import ModelForm
from django.shortcuts import render, redirect
from django import forms
from equipment.models import *


class ProfileForm(forms.ModelForm):
    class Meta:
        model = Profile
        exclude = ['user']
class RegisterForm(forms.Form):
    username = forms.CharField(label="Логин")
    email = forms.EmailField(label="Email", required=False)
    password = forms.CharField(label="Пароль", widget=forms.PasswordInput)
    password_confirm = forms.CharField(label="Подтвердите пароль", widget=forms.PasswordInput)

    def is_valid(self):
        valid = super(RegisterForm, self).is_valid()
        if self.cleaned_data['password'] != self.cleaned_data['password_confirm']:
            self.add_error("password_confirm", "Пароли не совпадают")
            return False
        return valid

class PostForm(ModelForm):
    class Meta:
        model = Post
        exclude = ['author']

class ProfileForm(forms.ModelForm):
    class Meta:
        model = Profile
        fields = ['profile_pic', 'user', 'firstname', 'lastname', 'city',
                  'bio',  'achievements', 'VK', 'Telegram', 'WhatsApp']