from django.contrib.auth.models import User
from django.contrib.auth.forms import UserCreationForm
from django import forms

from django import forms
from django.contrib.auth.forms import UserCreationForm
from datauploader.models import CustomUser

class CustomUserRegistrationForm(UserCreationForm):
    email = forms.EmailField(required=True)
    first_name = forms.CharField(required=True, max_length=100)
    middle_name = forms.CharField(required=False, max_length=100)
    last_name = forms.CharField(required=True, max_length=100)
    number = forms.IntegerField(required=True, label="Mobile Number")
    age = forms.IntegerField(required=True)
    city = forms.CharField(required=True, max_length=100)
    occupation = forms.CharField(required=True, max_length=100)

    class Meta:
        model = CustomUser
        fields = [
            'username', 'first_name', 'middle_name', 'last_name', 'age', 
            'number', 'occupation', 'email', 'password1', 'password2'
        ]

    def clean_email(self):
        email = self.cleaned_data.get('email')
        if CustomUser.objects.filter(email=email).exists():
            raise forms.ValidationError("This email is already in use.")
        return email



class UserLoginForm(forms.Form):
    username = forms.CharField(max_length=30)
    password = forms.CharField(widget=forms.PasswordInput())




class UserProfileForm(forms.Form):
    first_name = forms.CharField(
        label='First Name',
        max_length=30,
        widget=forms.TextInput(attrs={
            'class': 'form-control',
            'placeholder': 'Enter your first name'
        })
    )
    middle_name = forms.CharField(
        label='Middle Name',
        max_length=30,
        required=False,
        widget=forms.TextInput(attrs={
            'class': 'form-control',
            'placeholder': 'Enter your middle name'
        })
    )
    last_name = forms.CharField(
        label='Last Name',
        max_length=30,
        widget=forms.TextInput(attrs={
            'class': 'form-control',
            'placeholder': 'Enter your last name'
        })
    )
    age = forms.IntegerField(
        label='Age',
        widget=forms.NumberInput(attrs={
            'class': 'form-control',
            'placeholder': 'Enter your age'
        })
    )
    email = forms.EmailField(
        label='Email',
        widget=forms.EmailInput(attrs={
            'class': 'form-control',
            'placeholder': 'Enter your email',
            'required': True
        })
    )
    occupation = forms.CharField(
        label='Occupation',
        max_length=100,
        required=False,
        widget=forms.TextInput(attrs={
            'class': 'form-control',
            'placeholder': 'Enter your occupation'
        })
    )
    city = forms.CharField(
        label='Location',
        max_length=100,
        required=False,
        widget=forms.TextInput(attrs={
            'class': 'form-control',
            'placeholder': 'Enter your location'
        })
    )

    number = forms.CharField(
        label='Contact Number',
        max_length=15,
        required=False,  # Set to False if the field is optional
        widget=forms.TextInput(attrs={
            'class': 'form-control',
            'placeholder': 'Enter your contact number'
        })
    )

