import random
import string

from django.contrib.auth.decorators import login_required
from django.contrib.auth.forms import UserCreationForm
from django.contrib.auth.mixins import LoginRequiredMixin
from django.contrib.auth.views import LoginView, LogoutView
from django.shortcuts import render, get_object_or_404
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
    template_name = 'home.html'


class GroupView(TemplateView):
    model = Group
    template_name = 'group_view.html'
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


class GroupListView(LoginRequiredMixin, ListView):
    template_name = 'group_list.html'
    context_object_name = "groups"

    def get_queryset(self):
        return GroupUser.objects.filter(user_id=self.request.user.profile)


class GroupCreateView(LoginRequiredMixin, CreateView):
    model = Group
    template_name = 'group_new.html'
    fields = ['name', 'invite_url', 'admin_id']
    success_url = reverse_lazy('home')

    def generate_unique_url(self, length):
        urls = self.model.objects.all().values_list('invite_url', flat=True)
        while True:
            invite_url = ''.join(random.choices(string.ascii_lowercase + string.digits, k=length))
            if invite_url in urls:
                continue
            return invite_url

    def form_valid(self, form):
        form.instance.admin_id = self.request.user.profile
        form.instance.invite_url = self.generate_unique_url(10)
        form.instance.save()
        GroupUser(user_id=self.request.user.profile, group_id=form.instance).save()
        return super().form_valid(form)

@login_required()
def group_view(request, id):
    context = {}
    context["group"] = get_object_or_404(Group, pk=id)
    context["payments"] = Payment.objects.filter(group_id=id)
    context["user_costs"] = CostUser.objects.filter(user_id=request.user.profile, cost_id__group_id=id)
    context["balance"] = GroupUser.objects.get(user_id=request.user.profile, group_id=id)
    context["users_in_group"] = GroupUser.objects.filter(group_id=id)
    template = "group_view.html"

    return render(request, template_name=template, context=context)


class Login(LoginView):
    template_name = 'login.html'
    success_url = reverse_lazy('home')


class SignUpView(CreateView):
    form_class = SignUpForm
    success_url = reverse_lazy('login')
    template_name = 'signup.html'


class TemplateView(LogoutView):
    template_name = 'home.html'


class CostCreateView(LoginRequiredMixin, CreateView):
    model = Cost
    template_name = 'cost_new.html'
    fields = ['title', 'amount', 'payer_id', 'group_id']
    success_url = reverse_lazy('home')


class CostEditView(LoginRequiredMixin, UpdateView):
    model = Cost
    template_name = 'cost_edit.html'
    fields = '__all__'
    success_url = '/cost'


class CostDeleteView(LoginRequiredMixin, DeleteView):
    model = Cost
    template_name = 'cost_delete.html'
    success_url = '/cost'


class CostDetailView(DetailView):
    model = Cost
    template_name = 'cost_view.html'


class CostView(ListView):
    model = Cost
    template_name = 'costs_list.html'


