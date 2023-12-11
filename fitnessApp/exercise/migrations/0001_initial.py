# Generated by Django 5.0 on 2023-12-11 20:02

from django.db import migrations, models


class Migration(migrations.Migration):

    initial = True

    dependencies = [
    ]

    operations = [
        migrations.CreateModel(
            name='Tag',
            fields=[
                ('id', models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('name', models.CharField(max_length=50)),
            ],
        ),
        migrations.CreateModel(
            name='Exercise',
            fields=[
                ('id', models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('name', models.CharField(max_length=255, unique=True)),
                ('slug', models.SlugField(max_length=255, unique=True)),
                ('description', models.TextField(blank=True, null=True)),
                ('duration', models.PositiveIntegerField(blank=True, null=True)),
                ('image_url', models.URLField(blank=True, null=True)),
                ('difficulty', models.IntegerField(choices=[(0, 'EASY'), (50, 'MEDIUM'), (100, 'HARD'), (200, 'PRO')], default=0)),
                ('tags', models.ManyToManyField(blank=True, related_name='exercises', to='exercise.tag')),
            ],
        ),
    ]
