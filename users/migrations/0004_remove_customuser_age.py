# Generated by Django 4.1 on 2022-08-30 17:47

from django.db import migrations


class Migration(migrations.Migration):

    dependencies = [
        ('users', '0003_customuser_age'),
    ]

    operations = [
        migrations.RemoveField(
            model_name='customuser',
            name='age',
        ),
    ]
