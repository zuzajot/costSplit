import random
import string

from django.contrib.auth.decorators import login_required
from django.contrib.auth.mixins import LoginRequiredMixin
from django.contrib.auth.views import LoginView, LogoutView
from django.http import HttpResponseRedirect
from django.shortcuts import render, get_object_or_404
from django.template import RequestContext
from django.urls import reverse_lazy
from django.views.generic import ListView, DetailView, DeleteView, UpdateView, CreateView, TemplateView

from .forms import SignUpForm, LoginForm
from .models import Profile, Group, GroupUser, Cost, CostUser, Payment
from django.contrib.auth import login, authenticate
from django.shortcuts import render, redirect
from django.contrib import messages


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
    #form_class = UsersCostForm
    success_url = reverse_lazy('home')


    def get_form_kwargs(self):
        """ Passes the request object to the form class.
         This is necessary to only display members that belong to a given user"""

        kwargs = super(CostCreateView, self).get_form_kwargs()
        kwargs['request'] = self.request
        return kwargs


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


@login_required()
def cost_view(request, cost_id):
    context = {}
    context["cost"] = get_object_or_404(Group, pk=cost_id)
    context["user_costs"] = CostUser.objects.filter(user_id=request.user.profile, cost_id_=cost_id)
    context["balance"] = GroupUser.objects.get(user_id=request.user.profile, cost_id=cost_id)
    template = "cost_view.html"

    return render(request, template_name=template, context=context)


class GroupListView(LoginRequiredMixin, ListView):
    template_name = 'group_list.html'
    context_object_name = "groups"

    def get_queryset(self):
        return GroupUser.objects.filter(user_id=self.request.user.profile)


class CreateGroupView(LoginRequiredMixin, CreateView):
    template_name = "create_group.html"
    model = Group
    fields = ["name"]
    success_url = "/groups"

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
def group_view(request, group_id):
    context = {}
    context["group"] = get_object_or_404(Group, pk=group_id)
    context["payments"] = Payment.objects.filter(group_id=group_id)
    context["user_costs"] = CostUser.objects.filter(user_id=request.user.profile, cost_id__group_id=group_id)
    context["balance"] = GroupUser.objects.get(user_id=request.user.profile, group_id=group_id)
    context["users_in_group"] = GroupUser.objects.filter(group_id=group_id)
    template = "group_view.html"

    return render(request, template_name=template, context=context)


@login_required()
def accept_or_decline_invitation(request, url):
    try:
        group = Group.objects.get(invite_url=url)
    except Group.DoesNotExist as e:
        messages.error(request, "Dana grupa nie istnieje!")
        return redirect("group_list")

    if GroupUser.objects.filter(user_id=request.user.profile, group_id=group):
        messages.error(request, "Już jesteś w tej grupie!")
        return redirect("group_list")

    context = {"group": group}
    template = "aod_invitation.html"

    if request.POST.get("no"):
        return redirect("group_list")
    elif request.POST.get("yes"):
        messages.success(request, "Dodano nową grupę")
        GroupUser(user_id=request.user.profile, group_id=group).save()
        return redirect("group_list")

    return render(request, template_name=template, context=context)


def LoginRequest(request):
    if request.method == 'POST':
        form = LoginForm(request.POST)
        if form.is_valid():
            form.save()
            username = form.cleaned_data.get('username')
            password = form.cleaned_data.get('password1')
            user = authenticate(username=username, password=password)
            login(request, user)
    else:
        form = LoginForm()
    return render(request, 'home.html', {'form': form})

