# Generated by Django 4.2 on 2023-04-10 13:47

from django.db import migrations


class Migration(migrations.Migration):

    dependencies = [
        ('movies', '0004_rename_first_name_actor_name_remove_actor_last_name'),
    ]

    operations = [
        migrations.RenameField(
            model_name='director',
            old_name='first_name',
            new_name='name',
        ),
        migrations.RemoveField(
            model_name='director',
            name='last_name',
        ),
    ]