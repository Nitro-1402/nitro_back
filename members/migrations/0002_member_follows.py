# Generated by Django 4.2 on 2023-04-05 11:24

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('members', '0001_initial'),
    ]

    operations = [
        migrations.AddField(
            model_name='member',
            name='Follows',
            field=models.ManyToManyField(to='members.member'),
        ),
    ]
