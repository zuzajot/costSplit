from django.contrib.auth.forms import UserCreationForm
from django.contrib.auth.mixins import LoginRequiredMixin
from django.contrib.auth.views import LoginView, LogoutView
from django.shortcuts import render
from django.urls import reverse_lazy
from django.views.generic import ListView, DetailView, DeleteView, UpdateView, CreateView, TemplateView
from .models import Profile, Group, GroupUser, Cost, CostUser, Payment


class HomeView(TemplateView):
    model = Group
    template_name = 'home.html'
    paginate_by = 10

    def get_queryset(self):
        searching_name = self.request.GET.get('search_box', None)
        if searching_name is not None:
            return self.model.objects.all().filter(name__icontains=searching_name)
        else:
            return self.model.objects.all()


class GroupDetailView(DetailView):
    model = Group
    template_name = 'group_detail.html'


class GroupCreateView(LoginRequiredMixin, CreateView):
    model = Group
    template_name = 'group_new.html'
    fields = ['name', 'invite_url', 'admin_id']
    success_url = '/group'


class Login(LoginView):
    template_name = 'login.html'


class SignUpView(CreateView):
    form_class = UserCreationForm
    success_url = reverse_lazy('login')
    template_name = 'signup.html'


class TemplateView(LogoutView):
    model = Group
    template_name = 'home.html'
