from django.contrib.auth.forms import UserCreationForm
from django.contrib.auth.mixins import LoginRequiredMixin
from django.contrib.auth.views import LoginView, LogoutView
from django.shortcuts import render
from django.urls import reverse_lazy
from django.views.generic import ListView, DetailView, DeleteView, UpdateView, CreateView, TemplateView

from .forms import SignUpForm
from .models import Profile, Group, GroupUser, Cost, CostUser, Payment
from django.contrib.auth import login, authenticate
from django.shortcuts import render, redirect


def signup(request):
    if request.method == 'POST':
        form = SignUpForm(request.POST)
        if form.is_valid():
            form.save()
            username = form.cleaned_data.get('username')
            raw_password = form.cleaned_data.get('password1')
            user = authenticate(username=username, password=raw_password)
            login(request, user)
            return redirect('home')
    else:
        form = SignUpForm()
    return render(request, 'signup.html', {'form': form})


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
    success_url = reverse_lazy('home')


class Login(LoginView):
    template_name = 'login.html'
    success_url = reverse_lazy('home')


class SignUpView(CreateView):
    form_class = SignUpForm
    success_url = reverse_lazy('login')
    template_name = 'signup.html'


class TemplateView(LogoutView):
    template_name = 'home.html'

