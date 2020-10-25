from django.shortcuts import render
from django.views.generic import ListView, UpdateView, DetailView, CreateView, DeleteView

# Create your views here.

class GroupView(ListView):

    template_name = 'movies.html'

class SomeDetailView(DetailView):
    template_name = "details.html"
class Zuza(UpdateView):
    pass
