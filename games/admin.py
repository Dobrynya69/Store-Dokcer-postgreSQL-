from telnetlib import GA
from django.contrib import admin
from django.contrib.admin import ModelAdmin
from .models import *

class CommentInline(admin.TabularInline):
    model = Comment


class GradeInline(admin.TabularInline):
    model = Grade


class GameAdmin(ModelAdmin):
    inlines = [CommentInline, GradeInline]
    list_display = ('name', 'studio', 'playtime')


class GameInline(admin.TabularInline):
    model = Game


class StudioAdmin(ModelAdmin):
    inlines = [GameInline,]


admin.site.register(Grade)
admin.site.register(Comment)
admin.site.register(Game, GameAdmin)
admin.site.register(Studio, StudioAdmin)