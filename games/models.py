from datetime import datetime
from distutils.command.upload import upload
from urllib import request
from django.db import models
import uuid
from django.urls import reverse
from django.contrib.auth import get_user_model


class Studio(models.Model):
    name = models.CharField(max_length=30, unique=True)


    def __str__(self):
        return self.name


class Game(models.Model):
    id = models.UUIDField(primary_key=True, default=uuid.uuid4, editable=False)
    name = models.CharField(max_length=250)
    studio = models.ForeignKey(Studio, on_delete=models.CASCADE)
    description = models.TextField()
    playtime = models.DecimalField(max_digits=10, decimal_places=2)
    year = models.PositiveIntegerField()
    image = models.ImageField(upload_to='media/images/', null=True, blank=True)


    def __str__(self):
        return self.name

    def get_absolute_url(self):
        return reverse('game', kwargs={'pk': self.pk})


class Comment(models.Model):
    game = models.ForeignKey(Game, on_delete=models.CASCADE)
    user = models.ForeignKey(get_user_model(), on_delete=models.CASCADE)
    text = models.TextField()
    date = models.DateTimeField(default=datetime.now())
    
    