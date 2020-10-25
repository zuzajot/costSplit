from django.shortcuts import render
from django.views.generic import ListView, UpdateView, DetailView, CreateView, DeleteView

# Create your views here.

class GroupView(ListView):

    template_name = 'movies.html'



class ClassDadana_przez_marka(ListView):
    kto_to_dodal = "marek to dodal"
    template_name = 'Marek.html'

