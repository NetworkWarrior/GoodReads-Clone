# Generated by Django 3.1.14 on 2022-11-16 23:54

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('books', '0001_initial'),
    ]

    operations = [
        migrations.AddField(
            model_name='book',
            name='book_cover',
            field=models.ImageField(default='book_cover.png', upload_to=''),
        ),
    ]
