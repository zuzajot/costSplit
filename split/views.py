from django.contrib.auth.mixins import LoginRequiredMixin
from django.shortcuts import render, get_object_or_404
from django.contrib.auth.decorators import login_required
from django.views.generic import ListView, CreateView
from .models import GroupUser, Group, Payment, Cost, CostUser
import string
import random

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
def group_view(request, id):
    context = {}
    context["group"] = get_object_or_404(Group, pk=id)
    context["payments"] = Payment.objects.filter(group_id=id)
    context["costs"] = Cost.objects.filter(group_id=id)
    context["user_in_group"] = GroupUser.objects.get(user_id=request.user.profile, group_id=id)
    template = "group_view.html"

    return render(request, template_name=template, context=context)
