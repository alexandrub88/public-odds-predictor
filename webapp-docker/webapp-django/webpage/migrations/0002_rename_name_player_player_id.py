# Generated by Django 4.1.13 on 2024-02-05 16:43

from django.db import migrations


class Migration(migrations.Migration):

    dependencies = [
        ('webpage', '0001_initial'),
    ]

    operations = [
        migrations.RenameField(
            model_name='player',
            old_name='name',
            new_name='player_id',
        ),
    ]