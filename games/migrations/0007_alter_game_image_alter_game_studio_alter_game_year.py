# Generated by Django 4.1 on 2022-08-24 10:08

from django.db import migrations, models
import django.db.models.deletion


class Migration(migrations.Migration):

    dependencies = [
        ('games', '0006_alter_game_image'),
    ]

    operations = [
        migrations.AlterField(
            model_name='game',
            name='image',
            field=models.ImageField(upload_to='media/images/'),
        ),
        migrations.AlterField(
            model_name='game',
            name='studio',
            field=models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, to='games.studio'),
        ),
        migrations.AlterField(
            model_name='game',
            name='year',
            field=models.PositiveIntegerField(),
        ),
    ]
