from django.contrib.auth.mixins import LoginRequiredMixin
from django.http import HttpResponseRedirect
from django.shortcuts import render, get_object_or_404, redirect
from django.contrib.auth.decorators import login_required
from django.views.generic import ListView, CreateView
from .models import GroupUser, Group, Payment, Cost, CostUser
import string
import random
from django.contrib import messages

# Create your views here.


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
        context = {"group": group}
        template = "aod_invitation.html"
    except Group.DoesNotExist as e:
        messages.error(request, "Dana grupa nie istnieje!")
        return redirect("group_list")

    return render(request, template_name=template, context=context)





