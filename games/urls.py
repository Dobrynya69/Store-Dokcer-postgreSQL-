from django.urls import path
from .views import *

urlpatterns = [
    path('list/', GamesListView.as_view(), name='game_list'), 
    path('comment/<pk>/delete/', CommentDeleteView.as_view(), name='comment_delete'),
    path('comment/<pk>/edit/', CommentEditView.as_view(), name='comment_edit'),
    path('<pk>/comment/crete/', CommentCreateView.as_view(), name='comment_create'),
    path('<pk>/', GamesDetailView.as_view(), name='game'),
]
