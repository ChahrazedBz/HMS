# Generated by Django 5.2.1 on 2025-07-21 23:57

from django.db import migrations


class Migration(migrations.Migration):

    dependencies = [
        ('userauth', '0001_initial'),
    ]

    operations = [
        migrations.RemoveField(
            model_name='profile',
            name='email',
        ),
        migrations.RemoveField(
            model_name='profile',
            name='username',
        ),
    ]
