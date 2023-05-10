# Generated by Django 4.2.1 on 2023-05-10 11:49

from django.conf import settings
import django.core.validators
from django.db import migrations, models
import django.db.models.deletion
import movies.models


class Migration(migrations.Migration):

    initial = True

    dependencies = [
        migrations.swappable_dependency(settings.AUTH_USER_MODEL),
    ]

    operations = [
        migrations.CreateModel(
            name="Actor",
            fields=[
                (
                    "id",
                    models.BigAutoField(
                        auto_created=True,
                        primary_key=True,
                        serialize=False,
                        verbose_name="ID",
                    ),
                ),
                ("name", models.CharField(max_length=255)),
                ("photo", models.ImageField(upload_to=movies.models.movie_actor_path)),
                ("bio", models.TextField(null=True)),
                ("birth_date", models.DateField()),
            ],
        ),
        migrations.CreateModel(
            name="Director",
            fields=[
                (
                    "id",
                    models.BigAutoField(
                        auto_created=True,
                        primary_key=True,
                        serialize=False,
                        verbose_name="ID",
                    ),
                ),
                ("name", models.CharField(max_length=255)),
                (
                    "photo",
                    models.ImageField(upload_to=movies.models.movie_director_path),
                ),
                ("bio", models.TextField(null=True)),
                ("birth_date", models.DateField()),
            ],
        ),
        migrations.CreateModel(
            name="Movie",
            fields=[
                (
                    "id",
                    models.BigAutoField(
                        auto_created=True,
                        primary_key=True,
                        serialize=False,
                        verbose_name="ID",
                    ),
                ),
                ("title", models.CharField(max_length=255)),
                (
                    "thumbnail",
                    models.ImageField(upload_to=movies.models.movie_thumbnail_path),
                ),
                (
                    "movie_type",
                    models.CharField(
                        choices=[("M", "Movie"), ("S", "Series")],
                        default="M",
                        max_length=1,
                    ),
                ),
                (
                    "poster",
                    models.ImageField(upload_to=movies.models.movie_poster_path),
                ),
                ("description", models.TextField()),
                (
                    "meta_rating",
                    models.PositiveSmallIntegerField(
                        blank=True,
                        null=True,
                        validators=[django.core.validators.MaxValueValidator(100)],
                    ),
                ),
                (
                    "imdb_rating",
                    models.PositiveSmallIntegerField(
                        blank=True,
                        null=True,
                        validators=[django.core.validators.MaxValueValidator(100)],
                    ),
                ),
                ("publish_date", models.DateField()),
                ("country", models.CharField(max_length=255)),
                ("actors", models.ManyToManyField(to="movies.actor")),
                (
                    "director",
                    models.ForeignKey(
                        on_delete=django.db.models.deletion.PROTECT,
                        to="movies.director",
                    ),
                ),
            ],
        ),
        migrations.CreateModel(
            name="Series_season",
            fields=[
                (
                    "id",
                    models.BigAutoField(
                        auto_created=True,
                        primary_key=True,
                        serialize=False,
                        verbose_name="ID",
                    ),
                ),
                ("title", models.CharField(max_length=255)),
                ("season_number", models.PositiveBigIntegerField()),
                ("description", models.TextField()),
                ("publish_date", models.DateField()),
                (
                    "series",
                    models.ForeignKey(
                        on_delete=django.db.models.deletion.CASCADE, to="movies.movie"
                    ),
                ),
            ],
        ),
        migrations.CreateModel(
            name="Series_episode",
            fields=[
                (
                    "id",
                    models.BigAutoField(
                        auto_created=True,
                        primary_key=True,
                        serialize=False,
                        verbose_name="ID",
                    ),
                ),
                ("title", models.CharField(max_length=255)),
                ("episode_number", models.PositiveBigIntegerField()),
                ("description", models.TextField()),
                ("publish_date", models.DateField()),
                (
                    "season",
                    models.ForeignKey(
                        on_delete=django.db.models.deletion.CASCADE,
                        to="movies.series_season",
                    ),
                ),
            ],
        ),
        migrations.CreateModel(
            name="Rating",
            fields=[
                (
                    "id",
                    models.BigAutoField(
                        auto_created=True,
                        primary_key=True,
                        serialize=False,
                        verbose_name="ID",
                    ),
                ),
                (
                    "rating",
                    models.PositiveSmallIntegerField(
                        validators=[django.core.validators.MaxValueValidator(100)]
                    ),
                ),
                (
                    "movie",
                    models.ForeignKey(
                        on_delete=django.db.models.deletion.CASCADE, to="movies.movie"
                    ),
                ),
                (
                    "user",
                    models.ForeignKey(
                        on_delete=django.db.models.deletion.CASCADE,
                        to=settings.AUTH_USER_MODEL,
                    ),
                ),
            ],
        ),
        migrations.CreateModel(
            name="News",
            fields=[
                (
                    "id",
                    models.BigAutoField(
                        auto_created=True,
                        primary_key=True,
                        serialize=False,
                        verbose_name="ID",
                    ),
                ),
                ("title", models.CharField(max_length=255)),
                (
                    "thumbnail",
                    models.ImageField(upload_to=movies.models.news_thumbnail_path),
                ),
                ("photo", models.ImageField(upload_to=movies.models.news_photo_path)),
                ("description", models.TextField()),
                ("actors", models.ManyToManyField(blank=True, to="movies.actor")),
                ("directors", models.ManyToManyField(blank=True, to="movies.director")),
                ("movies", models.ManyToManyField(blank=True, to="movies.movie")),
            ],
        ),
        migrations.CreateModel(
            name="Category",
            fields=[
                (
                    "id",
                    models.BigAutoField(
                        auto_created=True,
                        primary_key=True,
                        serialize=False,
                        verbose_name="ID",
                    ),
                ),
                ("title", models.CharField(max_length=255)),
                ("movies", models.ManyToManyField(blank=True, to="movies.movie")),
            ],
        ),
    ]
