from django.urls import path
from .views import *

urlpatterns = [
    path('list/', GamesListView.as_view(), name='game_list'),
    path('favorites/', FavoriteItemsListView.as_view(), name='favorites'), 
    path('comment/<pk>/delete/', CommentDeleteView.as_view(), name='comment_delete'),
    path('comment/<pk>/edit/', CommentEditView.as_view(), name='comment_edit'),
    path('<pk>/comment/crete/', CommentCreateView.as_view(), name='comment_create'),
    path('<pk>/favorite/', FavoriteItemView.as_view(), name='favorite_item'),
    path('<pk>/grade/', GradeView.as_view(), name='grade'),
    path('<pk>/', GamesDetailView.as_view(), name='game'),
]
