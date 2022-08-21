from logging import PlaceHolder
from django.contrib.auth import get_user_model
from django.contrib.auth.forms import UserCreationForm, UserChangeForm
from allauth.socialaccount.forms import SignupForm
from django import forms

class CustomUserCreationForm(UserCreationForm):
    password1 = forms.CharField(widget=forms.PasswordInput(), label='Password')
    class Meta:
        model = get_user_model()
        fields = ('email', 'username', 'first_name')

class CustomSocialSignupForm(SignupForm):
    password = forms.CharField(widget=forms.PasswordInput(), label='Password')
    first_name = forms.CharField(max_length=20, label='Name')

    def save(self, request):
        user = super(CustomSocialSignupForm, self).save(request)
        user.set_password(request.POST['password'])
        user.save()
        return user

class CustomUserChangeForm(UserChangeForm):
    class Meta:
        model = get_user_model()
        fields = ('email', 'username', 'first_name')
