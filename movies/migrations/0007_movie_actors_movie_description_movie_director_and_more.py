# Generated by Django 4.2 on 2023-04-11 13:56

from django.db import migrations, models
import django.db.models.deletion
import movies.models


class Migration(migrations.Migration):

    dependencies = [
        ('movies', '0006_alter_actor_photo_delete_movie_meta'),
    ]

    operations = [
        migrations.AddField(
            model_name='movie',
            name='actors',
            field=models.ManyToManyField(to='movies.actor'),
        ),
        migrations.AddField(
            model_name='movie',
            name='description',
            field=models.TextField(default=''),
            preserve_default=False,
        ),
        migrations.AddField(
            model_name='movie',
            name='director',
            field=models.ForeignKey(default=1, on_delete=django.db.models.deletion.PROTECT, to='movies.director'),
            preserve_default=False,
        ),
        migrations.AddField(
            model_name='movie',
            name='imdb_rating',
            field=models.DecimalField(decimal_places=1, max_digits=2, null=True),
        ),
        migrations.AddField(
            model_name='movie',
            name='meta_rating',
            field=models.DecimalField(decimal_places=1, max_digits=2, null=True),
        ),
        migrations.AddField(
            model_name='movie',
            name='poster',
            field=models.ImageField(default=1, upload_to=movies.models.movie_poster_path),
            preserve_default=False,
        ),
        migrations.AddField(
            model_name='movie',
            name='publish_date',
            field=models.DateField(default='2022-01-01'),
            preserve_default=False,
        ),
    ]
