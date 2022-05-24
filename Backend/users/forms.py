from django import forms
from django.contrib.auth.models import User
from django.contrib.auth.forms import UserCreationForm
from .models import Profile

class UserRegisterForm(UserCreationForm):
    """Registration form by django."""
    email = forms.EmailField()

    class Meta:
        model = User
        fields = ['username',
                  'email', 
                  'password1',
                  'password2']


class UserUpdateForm(forms.ModelForm):
    """Update form by django."""
    email = forms.EmailField()

    class Meta:
        model = User
        fields = ['username',
                  'email', 
                  ]


class ProfileUpdateForm(forms.ModelForm):
    """Profile update form by django."""
    class Meta:
        model = Profile
        fields = ['image']