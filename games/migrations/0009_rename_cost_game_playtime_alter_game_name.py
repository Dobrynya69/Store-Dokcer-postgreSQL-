# Generated by Django 4.1 on 2022-08-24 12:51

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('games', '0008_alter_game_image'),
    ]

    operations = [
        migrations.RenameField(
            model_name='game',
            old_name='cost',
            new_name='playtime',
        ),
        migrations.AlterField(
            model_name='game',
            name='name',
            field=models.CharField(max_length=250),
        ),
    ]
