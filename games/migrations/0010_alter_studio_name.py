# Generated by Django 4.1 on 2022-08-24 15:52

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('games', '0009_rename_cost_game_playtime_alter_game_name'),
    ]

    operations = [
        migrations.AlterField(
            model_name='studio',
            name='name',
            field=models.CharField(max_length=30, unique=True),
        ),
    ]
