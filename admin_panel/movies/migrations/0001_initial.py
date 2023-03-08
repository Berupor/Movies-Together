# Generated by Django 4.1.1 on 2022-10-04 13:29

import uuid

import django.core.validators
import django.db.models.deletion
from django.db import migrations, models


class Migration(migrations.Migration):

    initial = True

    dependencies = []

    operations = [
        migrations.RunSQL("CREATE SCHEMA IF NOT EXISTS movies_content;"),
        migrations.CreateModel(
            name="FilmWork",
            fields=[
                (
                    "created",
                    models.DateTimeField(auto_now_add=True, verbose_name="created"),
                ),
                (
                    "modified",
                    models.DateTimeField(auto_now=True, verbose_name="modified"),
                ),
                (
                    "id",
                    models.UUIDField(
                        default=uuid.uuid4,
                        editable=False,
                        primary_key=True,
                        serialize=False,
                    ),
                ),
                (
                    "certificate",
                    models.CharField(
                        max_length=512, null=True, verbose_name="certificate"
                    ),
                ),
                (
                    "file_path",
                    models.FileField(
                        blank=True, null=True, upload_to="movies/", verbose_name="file"
                    ),
                ),
                ("title", models.CharField(max_length=255, verbose_name="title")),
                (
                    "description",
                    models.TextField(null=True, verbose_name="description"),
                ),
                (
                    "creation_date",
                    models.DateField(auto_now_add=True, verbose_name="creation_date"),
                ),
                (
                    "rating",
                    models.FloatField(
                        null=True,
                        validators=[
                            django.core.validators.MinValueValidator(0),
                            django.core.validators.MaxValueValidator(100),
                        ],
                        verbose_name="rating",
                    ),
                ),
                (
                    "type",
                    models.CharField(
                        choices=[("Movie", "Movie"), ("Tv_show", "Tv_show")],
                        max_length=25,
                        verbose_name="type",
                    ),
                ),
            ],
            options={
                "verbose_name": "Movie",
                "verbose_name_plural": "Movies",
                "db_table": 'movies_content"."film_work',
            },
        ),
        migrations.CreateModel(
            name="Genre",
            fields=[
                (
                    "created",
                    models.DateTimeField(auto_now_add=True, verbose_name="created"),
                ),
                (
                    "modified",
                    models.DateTimeField(auto_now=True, verbose_name="modified"),
                ),
                (
                    "id",
                    models.UUIDField(
                        default=uuid.uuid4,
                        editable=False,
                        primary_key=True,
                        serialize=False,
                    ),
                ),
                ("name", models.CharField(max_length=255, verbose_name="name")),
                (
                    "description",
                    models.TextField(null=True, verbose_name="description"),
                ),
            ],
            options={
                "verbose_name": "Genre",
                "verbose_name_plural": "Genres",
                "db_table": 'movies_content"."genre',
            },
        ),
        migrations.CreateModel(
            name="GenreFilmwork",
            fields=[
                (
                    "id",
                    models.UUIDField(
                        default=uuid.uuid4,
                        editable=False,
                        primary_key=True,
                        serialize=False,
                    ),
                ),
                ("created", models.DateTimeField(auto_now_add=True)),
            ],
            options={
                "verbose_name": "Genre Filmwork",
                "verbose_name_plural": "Genre Filmworks",
                "db_table": 'movies_content"."genre_film_work',
            },
        ),
        migrations.CreateModel(
            name="Person",
            fields=[
                (
                    "created",
                    models.DateTimeField(auto_now_add=True, verbose_name="created"),
                ),
                (
                    "modified",
                    models.DateTimeField(auto_now=True, verbose_name="modified"),
                ),
                (
                    "id",
                    models.UUIDField(
                        default=uuid.uuid4,
                        editable=False,
                        primary_key=True,
                        serialize=False,
                    ),
                ),
                (
                    "full_name",
                    models.CharField(max_length=255, verbose_name="full_name"),
                ),
                (
                    "gender",
                    models.TextField(
                        blank=True,
                        choices=[("male", "male"), ("female", "female")],
                        null=True,
                        verbose_name="gender",
                    ),
                ),
            ],
            options={
                "verbose_name": "Person",
                "verbose_name_plural": "Persons",
                "db_table": 'movies_content"."person',
            },
        ),
        migrations.CreateModel(
            name="PersonFilmwork",
            fields=[
                (
                    "id",
                    models.UUIDField(
                        default=uuid.uuid4,
                        editable=False,
                        primary_key=True,
                        serialize=False,
                    ),
                ),
                (
                    "role",
                    models.CharField(
                        choices=[
                            ("actor", "Actor"),
                            ("director", "Director"),
                            ("writer", "Writer"),
                        ],
                        max_length=255,
                        verbose_name="role",
                    ),
                ),
                ("created", models.DateTimeField(auto_now_add=True)),
                (
                    "film_work",
                    models.ForeignKey(
                        on_delete=django.db.models.deletion.CASCADE,
                        to="movies.filmwork",
                        verbose_name="Film work",
                    ),
                ),
                (
                    "person",
                    models.ForeignKey(
                        on_delete=django.db.models.deletion.CASCADE,
                        to="movies.person",
                        verbose_name="Person",
                    ),
                ),
            ],
            options={
                "verbose_name": "Person Filmwork",
                "verbose_name_plural": "Person Filmworks",
                "db_table": 'movies_content"."person_film_work',
            },
        ),
        migrations.AddIndex(
            model_name="person",
            index=models.Index(fields=["full_name"], name="person_full_name_idx"),
        ),
        migrations.AddField(
            model_name="genrefilmwork",
            name="film_work",
            field=models.ForeignKey(
                on_delete=django.db.models.deletion.CASCADE,
                to="movies.filmwork",
                verbose_name="Film work",
            ),
        ),
        migrations.AddField(
            model_name="genrefilmwork",
            name="genre",
            field=models.ForeignKey(
                on_delete=django.db.models.deletion.CASCADE,
                to="movies.genre",
                verbose_name="Genre",
            ),
        ),
        migrations.AddField(
            model_name="filmwork",
            name="genres",
            field=models.ManyToManyField(
                through="movies.GenreFilmwork", to="movies.genre"
            ),
        ),
        migrations.AddField(
            model_name="filmwork",
            name="persons",
            field=models.ManyToManyField(
                through="movies.PersonFilmwork", to="movies.person"
            ),
        ),
        migrations.AddConstraint(
            model_name="personfilmwork",
            constraint=models.UniqueConstraint(
                fields=("person", "film_work", "role"), name="film_work_person_idx"
            ),
        ),
        migrations.AddConstraint(
            model_name="genrefilmwork",
            constraint=models.UniqueConstraint(
                fields=("genre", "film_work"), name="film_work_genre_idx"
            ),
        ),
        migrations.AddIndex(
            model_name="filmwork",
            index=models.Index(
                fields=["creation_date"], name="film_work_creation_date_idx"
            ),
        ),
    ]
