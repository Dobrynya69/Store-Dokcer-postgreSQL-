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


    def post(self, request, *args, **kwargs):
        for i in range(1, 5):
            url = f"https://rawg-video-games-database.p.rapidapi.com/games?key=9abdc41cb9364cca828cf48c984ab392&page={i}"
            headers = {'x-rapidapi-key': "14dc4a90c9msh94b4ad390a5f68fp168792jsn5502a433c731", 'x-rapidapi-host': "rawg-video-games-database.p.rapidapi.com"}
            r = requests.get(url=url, headers=headers)
            answer = json.loads(r.text)

            url_detail = f'https://rawg-video-games-database.p.rapidapi.com/games/{answer["results"][1]["id"]}?key=9abdc41cb9364cca828cf48c984ab392'
            headers_detail = {'X-RapidAPI-Key': '14dc4a90c9msh94b4ad390a5f68fp168792jsn5502a433c731', 'X-RapidAPI-Host': 'rawg-video-games-database.p.rapidapi.com'}
            r_detail = requests.get(url=url_detail, headers=headers_detail)
            answer_detail = json.loads(r_detail.text)

            stud = Studio.objects.get(name="GGWP")
            for i in range(0, 20):
                game = answer["results"][i] 
                new_game = Game.objects.create(name=game["name"], studio=stud, description=f"{game['rating']} rating", playtime=game["playtime"], year=int(game["released"][:4]), image=game["background_image"])
                response = requests.get(game["background_image"])

                new_game.image.save(urlparse(game["background_image"]).path.split('/')[-1], ContentFile(response.content), save=True)

                url_detail = f'https://rawg-video-games-database.p.rapidapi.com/games/{answer["results"][i]["id"]}?key=9abdc41cb9364cca828cf48c984ab392'
                headers_detail = {'X-RapidAPI-Key': '14dc4a90c9msh94b4ad390a5f68fp168792jsn5502a433c731', 'X-RapidAPI-Host': 'rawg-video-games-database.p.rapidapi.com'}
                r_detail = requests.get(url=url_detail, headers=headers_detail)
                answer_detail = json.loads(r_detail.text)
                new_game.description = answer_detail["description"]
                publisher = Studio.objects.get_or_create(name=answer_detail["publishers"][0]["name"])[0]
                new_game.studio = publisher
                new_game.save()


        return render(request=request, template_name='storepages/home.html')