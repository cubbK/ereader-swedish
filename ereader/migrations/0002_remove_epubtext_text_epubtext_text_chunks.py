# Generated by Django 4.2.19 on 2025-02-17 22:01

import django.contrib.postgres.fields
from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('ereader', '0001_initial'),
    ]

    operations = [
        migrations.RemoveField(
            model_name='epubtext',
            name='text',
        ),
        migrations.AddField(
            model_name='epubtext',
            name='text_chunks',
            field=django.contrib.postgres.fields.ArrayField(base_field=models.TextField(), blank=True, default=list, size=None),
        ),
    ]
