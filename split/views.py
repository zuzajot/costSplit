from django.shortcuts import render
from django.views.generic import TemplateView, ListView, UpdateView, DetailView, CreateView, DeleteView

# Create your views here.


class HomeView(TemplateView):
    template_name = 'split/home.html'
