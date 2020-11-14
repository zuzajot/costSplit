import random
import string

from django.contrib.auth.decorators import login_required
from django.contrib.auth.forms import AuthenticationForm
from django.contrib.auth.mixins import LoginRequiredMixin
from django.contrib.auth.views import LogoutView, PasswordResetCompleteView, PasswordResetConfirmView, \
    PasswordResetDoneView, PasswordResetView, PasswordChangeView, PasswordChangeDoneView
from django.http import HttpResponseRedirect
from django.shortcuts import render, redirect, get_object_or_404
from django.urls import reverse_lazy, reverse
from django.views.generic import ListView, DetailView, DeleteView, UpdateView, CreateView

from .forms import SignUpForm
from .models import Profile, Group, GroupUser, Cost, CostUser, Payment
from django.contrib.auth import login, authenticate
from django.contrib import messages


def login_request(request):
    if request.method == 'POST':
        form = AuthenticationForm(data=request.POST)
        print(form)

        if form.is_valid():
            username = form.cleaned_data.get('username')
            password = form.cleaned_data.get('password')
            user = authenticate(username=username, password=password)
            if user is not None:
                login(request, user)
                return HttpResponseRedirect("/groups")
    else:
        form = AuthenticationForm()
    return render(request, 'home.html', {'form': form})


def signup(request):
    if request.method == 'POST':
        form = SignUpForm(request.POST)
        if form.is_valid():
            form.save()
            username = form.cleaned_data.get('username')
            raw_password = form.cleaned_data.get('password1')
            user = authenticate(username=username, password=raw_password)
            login(request, user)
            return HttpResponseRedirect('/groups')
    else:
        form = SignUpForm()
    return render(request, 'signup.html', {'form': form})


class LogoutView(LogoutView):
    template_name = 'home.html'


class CostCreateView(LoginRequiredMixin, CreateView):
    model = Cost
    template_name = 'cost_new.html'
    success_url = reverse_lazy('group_view')

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

    def get(self, request, **kwargs):
        self.object = self.get_object()
        current_user = request.user
        context = self.get_context_data()

        users_involved = [self.object.payer_id]
        for cost_user in list(context["cost_users"]):
            users_involved.append(cost_user.user_id.user)

        if current_user not in users_involved:
            messages.error(request, "Zabłądziłeś!")
            return redirect("/groups")

        return self.render_to_response(context)

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        context["cost_users"] = CostUser.objects.filter(cost_id=self.object.id)
        return context


class GroupListView(LoginRequiredMixin, ListView):
    template_name = 'group_list.html'
    context_object_name = "groups"

    def get_queryset(self):
        return GroupUser.objects.filter(user_id=self.request.user.profile)


class CreateGroupView(LoginRequiredMixin, CreateView):
    template_name = "create_group.html"
    model = Group
    fields = ["name"]

    def form_valid(self, form):
        form.instance.admin_id = self.request.user.profile
        form.instance.invite_url = self.generate_unique_url(10)
        form.instance.save()
        GroupUser(user_id=self.request.user.profile, group_id=form.instance).save()
        return HttpResponseRedirect(reverse("group_view", args=(form.instance.id,)))

    def generate_unique_url(self, length):
        urls = self.model.objects.all().values_list('invite_url', flat=True)
        while True:
            invite_url = ''.join(random.choices(string.ascii_lowercase + string.digits, k=length))
            if invite_url in urls:
                continue
            return invite_url


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
        return redirect(reverse("group_view", args=(group.id,)))

    context = {"group": group}
    template = "aod_invitation.html"

    if request.POST.get("no"):
        return redirect("group_list")
    elif request.POST.get("yes"):
        messages.success(request, "Dodano nową grupę!")
        GroupUser(user_id=request.user.profile, group_id=group).save()
        return redirect(reverse("group_view", args=(group.id,)))

    return render(request, template_name=template, context=context)


class GroupDeleteView(LoginRequiredMixin, DeleteView):
    model = Group
    template_name = "group_delete.html"
    success_url = "/groups"

    def dispatch(self, request, *args, **kwargs):
        group = self.get_object()
        if not group.admin_id == self.request.user.profile:
            messages.error(self.request, "Chyba zabłądziłeś przyjacielu")
            return redirect("group_view", group_id=self.kwargs["pk"])

        for user in GroupUser.objects.filter(group_id=self.kwargs["pk"]):
            if not user.balance == 0:
                messages.error(self.request, "Grupowy bilans wszystkich użytkownikow musi wynosić 0!")
                return redirect("group_view", group_id=self.kwargs["pk"])

        messages.success(self.request, "Usunięto grupę!")
        return super(GroupDeleteView, self).dispatch(request, *args, **kwargs)


class CostCreateView(LoginRequiredMixin, CreateView):
    model = Cost
    template_name = 'cost_new.html'
    fields = [
        "title",
        "amount",
    ]

    def form_valid(self, form):
        if form.instance.amount <= 0:
            messages.error(self.request, "Nie możesz dodać ujemnego wydatku!")
            return HttpResponseRedirect(self.request.META.get('HTTP_REFERER'))

        elif len(self.request.POST.getlist('payers')) < 2:
            messages.error(self.request, "Dodaj więcej płacących!")
            return HttpResponseRedirect(self.request.META.get('HTTP_REFERER'))

        form.instance.payer_id = self.request.user.profile
        group = Group.objects.get(id=self.kwargs["group_id"])
        form.instance.group_id = group
        form.instance.save()

        creator = GroupUser.objects.get(user_id=self.request.user.profile, group_id=group)
        users_involved = [creator]
        for user_id in self.request.POST.getlist('payers'):
            user = Profile.objects.get(id=user_id)
            CostUser(user_id=user, cost_id=form.instance).save()
            users_involved.append(GroupUser.objects.get(user_id=user, group_id=group))
        distribute_cost_among_users(users_involved, form.instance.amount, creator)

        return HttpResponseRedirect(reverse("group_view", args=(group.id,)))

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        group = Group.objects.get(id=self.kwargs["group_id"])
        context["group_users"] = GroupUser.objects.filter(group_id=group)
        context["group"] = group
        return context


def distribute_cost_among_users(users, amount, creator):
    number_of_paying_users = len(users)-1
    users = list(set(users))
    for user in users:
        if user is creator:
            if len(users) > number_of_paying_users:
                money = amount
            else:
                money = amount - round(amount/number_of_paying_users, 2)
            user.balance += money
            user.save()
            user.user_id.balance += money
            user.user_id.save()
        else:
            money = round(amount/number_of_paying_users, 2)
            user.balance -= money
            user.save()
            user.user_id.balance -= money
            user.user_id.save()


class CostEditView(LoginRequiredMixin, UpdateView):
    model = Cost
    template_name = 'cost_edit.html'
    fields = '__all__'
    success_url = '/cost'


class CostDeleteView(LoginRequiredMixin, DeleteView):
    model = Cost
    template_name = 'cost_delete.html'
    # success_url = '/cost'

    def get_success_url(self):
        return reverse('group_view', kwargs={'group_id': self.object.group_id.id})
    
    def delete(self, request, *args, **kwargs):

        return super(CostDeleteView, self).delete(self, request, *args, **kwargs)


def revert_users_balance(cost_id, group_id, amount):
    users = CostUser.objects.filter(cost_id=cost_id).values_list('user_id')
    for user in users:
        GroupUser.objects.get(user_id=user.user_id.id, group_id=group_id).balance



class PasswordReset(PasswordResetView):
    email_template_name = 'templates/password_reset_form.html'
    success_url = reverse_lazy('accounts/password_reset/')


class PasswordResetDone(PasswordResetDoneView):
    template_name = 'templates/password_reset_done.html'
    success_url = reverse_lazy('accounts/password_reset/done/')


class PasswordResetConfirm(PasswordResetConfirmView):
    template_name = 'templates/password_reset_confirm.html'
    success_url = reverse_lazy('reset/<uidb64>/<token>')


class PasswordResetComplete(PasswordResetCompleteView):
    template_name = 'templates/password_reset_complete.html'
    success_url = reverse_lazy('reset/done/')


class PasswordChange(PasswordChangeView):
    template_name = 'templates/password_change.html'
    success_url = reverse_lazy('accounts/password_change/')


class PasswordChangeDone(PasswordChangeDoneView):
    template_name = 'templates/password_change_done.html'
    success_url = reverse_lazy('accounts/password_change/done/')


class MakePaymentView(LoginRequiredMixin, CreateView):
    model = Payment
    template_name = "make_payment.html"
    fields = ["amount"]
    success_url = "/groups"

    def form_valid(self, form):
        current_user = self.request.user.profile
        group = Group.objects.get(id=self.kwargs["group_id"])
        current_user_group = GroupUser.objects.get(user_id=current_user, group_id=group)

        if current_user_group.balance >= 0:
            messages.error(self.request, "Nie możesz zapłacić, będąc na plusie!")
            return HttpResponseRedirect(reverse("group_view", args=(group.id,)))

        if form.instance.amount > -current_user_group.balance or form.instance.amount < 0:
            messages.error(self.request, "Podałeś złą kwotę!")
            return HttpResponseRedirect(self.request.META.get('HTTP_REFERER'))

        distribute_money(form.instance.amount, group)

        form.instance.group_id = group
        form.instance.user_id = current_user
        current_user_group.balance += form.instance.amount
        current_user_group.save()
        current_user.balance += form.instance.amount
        current_user.save()
        messages.success(self.request, f"Spłacono {form.instance.amount}!")
        return HttpResponseRedirect(reverse("group_view", args=(group.id,)))

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        user_balance = GroupUser.objects.get(group_id=self.kwargs["group_id"], user_id=self.request.user.profile)
        context["user_balance"] = user_balance
        context["creditors"] = users_with_positive_balance(self.kwargs["group_id"])
        return context



def distribute_money(amount, group):
    for user in rates_of_distribution(group):
        user[0].balance = round(user[0].balance-(amount*user[1]), 2)
        user[0].save()
        user[0].user_id.balance = round(user[0].user_id.balance-(amount*user[1]), 2)
        user[0].user_id.save()


def rates_of_distribution(group):
    users = users_with_positive_balance(group)
    sum_of_money = sum_of_money_owned(group)
    rates = []
    for user in users:
        rates.append((user, (-user.balance)/sum_of_money))
    return rates


def sum_of_money_owned(group):
    sum_of_money = 0
    for user in users_with_positive_balance(group):
        sum_of_money += (-user.balance)
    return sum_of_money


def users_with_positive_balance(group):
    return GroupUser.objects.filter(group_id=group, balance__gt=0)


def costs_and_payments_view(request):
    context = {}
    context["costs"] = CostUser.objects.filter(user_id=request.user.profile)
    context["payments"] = Payment.objects.filter(user_id=request.user.profile)
    template = "user_history.html"

    return render(request, template_name=template, context=context)
