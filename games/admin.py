from telnetlib import GA
from django.contrib import admin
from django.contrib.admin import ModelAdmin
from .models import *


class GameAdmin(ModelAdmin):

    list_display = ('name', 'studio', 'playtime')


class GameInline(admin.TabularInline):
    model = Game


class StudioAdmin(ModelAdmin):
    inlines = [GameInline,]


admin.site.register(Game, GameAdmin)
admin.site.register(Studio, StudioAdmin)