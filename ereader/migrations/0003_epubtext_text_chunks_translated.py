# Generated by Django 4.2.19 on 2025-02-18 11:08

import django.contrib.postgres.fields
from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('ereader', '0002_remove_epubtext_text_epubtext_text_chunks'),
    ]

    operations = [
        migrations.AddField(
            model_name='epubtext',
            name='text_chunks_translated',
            field=django.contrib.postgres.fields.ArrayField(base_field=models.TextField(), blank=True, default=list, size=None),
        ),
    ]
