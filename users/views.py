from django.shortcuts import render, redirect
from django.urls import reverse_lazy
from django.views.generic import *
from django.contrib.auth.mixins import LoginRequiredMixin, UserPassesTestMixin
from django.contrib.auth import get_user_model
from .forms import *


class UserEditView(LoginRequiredMixin, UserPassesTestMixin, UpdateView):
    model = get_user_model()
    fields = ['first_name', 'image']
    context_object_name = 'form'
    template_name = 'users/edit.html'
    success_url = reverse_lazy('home')


    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        context['pk'] = self.kwargs['pk']
        return context


    def test_func(self):
        edit_user = self.model.objects.get(pk=self.kwargs['pk'])
        user = self.request.user
        return edit_user == user
