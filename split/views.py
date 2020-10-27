from django.contrib.auth.mixins import LoginRequiredMixin
from django.shortcuts import render
from django.contrib.auth.decorators import login_required
from django.views.generic import ListView, UpdateView, DetailView, CreateView, DeleteView
from . import db_operations as db
from .models import GroupUser


# Create your views here.


class GroupListView(LoginRequiredMixin, ListView):
    template_name = 'group_list.html'
    context_object_name = 'groups'

    def get_queryset(self):
        return GroupUser.filter(user_id=self.request.user)
