# Generated by Django 4.1.3 on 2022-11-27 06:09

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('books', '0007_author_born'),
    ]

    operations = [
        migrations.AddField(
            model_name='author',
            name='residency',
            field=models.CharField(default=1, max_length=150),
            preserve_default=False,
        ),
    ]