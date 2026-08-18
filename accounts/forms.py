from django import forms
from django.contrib.auth.forms import UserCreationForm
from .models import User
from .models import CompanyProfile


class RegisterForm(UserCreationForm):
    role = forms.ChoiceField(choices=User.Role.choices)
    email = forms.EmailField(required=True)

    class Meta:  # type: ignore
        model = User
        fields = ["username", "email", "role", "password1", "password2"]


class CompanyProfileForm(forms.ModelForm):
    class Meta:
        model = CompanyProfile
        fields = ["company_name", "company_website", "company_description"]
