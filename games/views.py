from django.shortcuts import render
from django.views.generic import *
from .models import *


class GamesListView(ListView):
    model = Game
    template_name = 'games/list.html'
    context_object_name = 'games'


class GamesDetailView(DetailView):
    model = Game
    template_name = 'games/detail.html'
    context_object_name = 'game'