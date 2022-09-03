from django.urls import path
from .views import *
urlpatterns = [
    path('<pk>/edit/', UserEditView.as_view(), name='user_edit'),
]
