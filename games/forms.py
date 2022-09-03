from django import forms
from .models import *


SORT_CHOICES =(
    ('name', 'Name↓'),
    ('-name', 'Name↑'), 
    ('playtime', 'Play time↓'), 
    ('-playtime', 'Play time↑'), 
    ('year', 'Year↓'),
    ('-year', 'Year↑'),
)


def studio_choices():
    STUDIO_CHOICES = []
    studios = []
    for studio in Studio.objects.all():
        studios.append(studio.pk)

    for studio_pk in studios:
        STUDIO_CHOICES.append((studio_pk, Studio.objects.get(pk=studio_pk).name))

    return tuple(STUDIO_CHOICES)


class GameSortForm(forms.Form):
    name = forms.CharField(max_length=260, required=False, widget=forms.TextInput(attrs={'placeholder':'Enter name of the game'}))
    order = forms.ChoiceField(choices=SORT_CHOICES, required=False)
    studio = forms.MultipleChoiceField(
            widget = forms.CheckboxSelectMultiple,
            choices = studio_choices(),
            required=False
    )


class CommentCreateForm(forms.Form):
    text = forms.CharField(widget=forms.TextInput(attrs={'placeholder':'Comment'}), label='')


class GradeForm(forms.ModelForm):
    number = forms.IntegerField(min_value=1, max_value=5, label='', widget=forms.TextInput(attrs={'placeholder':'Send or change grade (1 - 5)'}))
    class Meta:
        model = Grade
        fields = ('number',)