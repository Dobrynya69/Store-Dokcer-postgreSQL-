from datetime import datetime
from distutils.command.upload import upload
from itertools import count
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


    def get_grade(self):
        objects = Grade.objects.filter(game=self)
        if objects.count() > 0:
            grade = 0
            for g in objects:
                grade += g.number
            grade = int(grade // objects.count())
            return grade
        else:
            return 0


    def get_grade_by_user(self, user):
        try:
            grade = Grade.objects.get(game=self, user=user)
        except Grade.DoesNotExist:
            return 0

        return grade.number


    def get_absolute_url(self):
        return reverse('game', kwargs={'pk': self.pk})


class Comment(models.Model):
    game = models.ForeignKey(Game, on_delete=models.CASCADE)
    user = models.ForeignKey(get_user_model(), on_delete=models.CASCADE)
    text = models.TextField()
    date = models.DateTimeField(default=datetime.now())


    def __str__(self):
        return f'{self.user} - {self.game} ({self.pk})'


class Grade(models.Model):
    game = models.ForeignKey(Game, on_delete=models.CASCADE)
    user = models.ForeignKey(get_user_model(), on_delete=models.CASCADE)
    number = models.PositiveSmallIntegerField(default=1)


    def __str__(self):
        return f'{self.user} - {self.game} ({self.pk})'

    @staticmethod
    def get_grate(game):
        objects = Grade.objects.filter(game=game)
        if objects.count() > 0:
            grade = 0
            for g in objects:
                grade += g.number
            grade = int(grade // objects.count())
            return grade
        else:
            return 0
    
    
