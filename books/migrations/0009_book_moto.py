# Generated by Django 4.1.3 on 2022-11-27 07:44

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('books', '0008_author_residency'),
    ]

    operations = [
        migrations.AddField(
            model_name='book',
            name='moto',
            field=models.CharField(default=1, max_length=150),
            preserve_default=False,
        ),
    ]