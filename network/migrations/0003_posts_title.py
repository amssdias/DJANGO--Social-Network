# Generated by Django 3.0.8 on 2020-10-12 00:47

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('network', '0002_likes_posts'),
    ]

    operations = [
        migrations.AddField(
            model_name='posts',
            name='title',
            field=models.CharField(default=None, max_length=100),
            preserve_default=False,
        ),
    ]
