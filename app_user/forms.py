from django import forms
from django.contrib.auth.forms import UserCreationForm, UserChangeForm
from django.contrib.auth.models import User
from .models import UserProfile

class SignUpForm(UserCreationForm):
    username = forms.CharField(max_length=30)
    email = forms.EmailField(
        max_length=54)
    first_name = forms.CharField(
        max_length=40, help_text='First Name')
    last_name = forms.CharField(
        max_length=40, help_text='Last Name')
    class Meta:
        model=User
        fields =('username', 'email', 'first_name', 'last_name', 'password1', 'password2')

class UserUpdateForm(UserChangeForm):
    class Meta:
        model = User
        fields = ('username', 'email', 'first_name', 'last_name')
        widgets = {
            'username': forms.TextInput(attrs={'class': 'form-control', 'placeholder': 'username'}),
            'email': forms.TextInput(attrs={'class': 'form-control', 'placeholder': 'Email'}),
            'first_name': forms.TextInput(attrs={'class': 'form-control', 'placeholder': 'First Name'}),
            'last_name': forms.TextInput(attrs={'class': 'form-control', 'placeholder': 'Last Name'}),
        }

class ProfileUpdateForm(forms.ModelForm):
    class Meta:
        model = UserProfile
        fields = ('phone', 'address', 'city', 'country', 'zipcode', 'image')
        widgets = {
            'phone': forms.TextInput(attrs={'class': 'form-control', 'placeholder': 'Contact Number'}),
            'city': forms.TextInput(attrs={'class': 'form-control', 'placeholder': 'City'}),
            'zipcode': forms.TextInput(attrs={'class': 'form-control', 'placeholder': 'Zip Code'}),
            'address': forms.Textarea(attrs={'class': 'form-control', 'placeholder': 'Address'}),
            'country': forms.TextInput(attrs={'class': 'form-control', 'placeholder': 'Country'}),
            'image': forms.FileInput(attrs={'class': 'custom-file-label'}),
        }
