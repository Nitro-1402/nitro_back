# Generated by Django 4.2.1 on 2023-07-01 21:09

from django.db import migrations


class Migration(migrations.Migration):

    dependencies = [
        ("members", "0006_alter_subscribe_unique_together_and_more"),
        ("movies", "0004_remove_series_episode_description_and_more"),
    ]

    operations = [
        migrations.AlterUniqueTogether(
            name="rating",
            unique_together={("profile", "movie")},
        ),
    ]
