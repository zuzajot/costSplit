from django.contrib.auth.forms import UserCreationForm
from django.contrib.auth.views import LoginView, LogoutView, PasswordResetView, PasswordResetDoneView, \
    PasswordResetCompleteView, PasswordResetConfirmView, PasswordChangeView, PasswordChangeDoneView
from django.shortcuts import render, redirect
from django.urls import reverse_lazy
from django.views.generic import CreateView


class Login(LoginView):
    template_name = 'accounts/login.html'


class TemplateView(LogoutView):
    template_name = 'home.html'


class SignUpView(CreateView):
    form_class = UserCreationForm
    success_url = reverse_lazy('login')
    template_name = 'accounts/signup.html'


class PasswordReset(PasswordResetView):
    email_template_name = 'accounts/password_reset_form.html'
    success_url = reverse_lazy('accounts/password_reset/')


class PasswordResetDone(PasswordResetDoneView):
    template_name = 'accounts/password_reset_done.html'
    success_url = reverse_lazy('accounts/password_reset/done/')

class PasswordResetConfirm(PasswordResetConfirmView):
    template_name = 'accounts/password_reset_confirm.html'
    success_url = reverse_lazy('reset/<uidb64>/<token>')


class PasswordResetComplete(PasswordResetCompleteView):
    template_name = 'accounts/password_reset_complete.html'
    success_url = reverse_lazy('reset/done/')


class PasswordChange(PasswordChangeView):
    template_name = 'accounts/password_change.html'
    success_url = reverse_lazy('accounts/password_change/')


class PasswordChangeDone(PasswordChangeDoneView):
    template_name = 'accounts/password_change_done.html'
    success_url = reverse_lazy('accounts/password_change/done/')
