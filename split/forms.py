import form as form
from django import forms
from django.contrib.auth.forms import UserCreationForm
from django.contrib.auth.models import User

from .models import Cost, GroupUser, Profile


class SignUpForm(UserCreationForm):
    email = forms.EmailField(max_length=254, help_text='')

    class Meta:
        model = User
        fields = ('username', 'email', 'password1', 'password2', )


class UsersCostForm(forms.ModelForm):

    def __init__(self, *args, **kwargs):
        """ Grants access to the request object so that only members of the current user
        are given as options"""

        self.request = kwargs.pop('request')
        super(UsersCostForm, self).__init__(*args, **kwargs)
        self.fields['users'].queryset = Profile.objects.filter(
            user=self.request.user)

    class Meta:
        model = Cost
        fields = ('title', 'amount', 'payer_id', 'group_id', 'users',)
        users = forms.ModelMultipleChoiceField(queryset=GroupUser.objects.all(), widget=forms.CheckboxSelectMultiple)
