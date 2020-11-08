# import form as form
from django import forms
from django.contrib.auth.forms import UserCreationForm
from django.contrib.auth.models import User
from django.core.validators import MinLengthValidator

from .models import Cost, GroupUser, Profile


class SignUpForm(UserCreationForm):
    email = forms.EmailField(max_length=254, help_text='')

    class Meta:
        model = User
        fields = ('username', 'email', 'password1', 'password2', )


class UsersCostForm(forms.ModelForm):

    class Meta:
        model = Cost
        fields = ('title', 'amount')

    members = forms.ModelMultipleChoiceField(
        queryset=User.objects.all(),
        widget=forms.CheckboxSelectMultiple
    )
