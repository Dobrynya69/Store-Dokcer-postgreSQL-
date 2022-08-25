from django.urls import path
from .views import *

urlpatterns = [
    path('list/', GamesListView.as_view(), name='game_list'),
    path('<pk>/', GamesDetailView.as_view(), name='game'),
]
