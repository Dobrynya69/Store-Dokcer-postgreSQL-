# Generated by Django 4.1 on 2022-08-24 09:41

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('games', '0005_game_image_game_year'),
    ]

    operations = [
        migrations.AlterField(
            model_name='game',
            name='image',
            field=models.ImageField(blank=True, null=True, upload_to='media/images/'),
        ),
    ]