# Generated by Django 4.2.1 on 2023-05-21 16:37

import datetime
from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ("movies", "0001_initial"),
    ]

    operations = [
        migrations.AddField(
            model_name="news",
            name="publish_date",
            field=models.DateField(blank=True, default=datetime.date.today),
        ),
    ]