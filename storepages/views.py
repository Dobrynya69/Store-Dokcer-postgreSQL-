from ast import For
from unicodedata import name
from django.shortcuts import render
from django.views.generic import View
import json
import requests
from games.models import *
from django.core.files import File
from django.core.files.temp import NamedTemporaryFile
from urllib.parse import urlparse
from django.core.files.base import ContentFile

class HomeView(View):

    def get(self, request, *args, **kwargs):
        return render(request=request, template_name='storepages/home.html')