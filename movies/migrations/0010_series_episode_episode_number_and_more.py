# Generated by Django 4.2 on 2023-04-13 12:07

import django.core.validators
from django.db import migrations, models
import django.db.models.deletion


class Migration(migrations.Migration):

    dependencies = [
        ('movies', '0009_alter_movie_imdb_rating_alter_movie_meta_rating'),
    ]

    operations = [
        migrations.AddField(
            model_name='series_episode',
            name='episode_number',
            field=models.PositiveBigIntegerField(default=1),
            preserve_default=False,
        ),
        migrations.AddField(
            model_name='series_season',
            name='season_number',
            field=models.PositiveBigIntegerField(default=1),
            preserve_default=False,
        ),
        migrations.AlterField(
            model_name='rating',
            name='rating',
            field=models.PositiveSmallIntegerField(validators=[django.core.validators.MaxValueValidator(100)]),
        ),
        migrations.AlterField(
            model_name='series_episode',
            name='season',
            field=models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, to='movies.series_season'),
        ),
        migrations.AlterField(
            model_name='series_season',
            name='series',
            field=models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, to='movies.movie'),
        ),
    ]