# Generated by Django 3.0.8 on 2020-10-19 01:14

from django.conf import settings
from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('network', '0006_auto_20201019_0011'),
    ]

    operations = [
        migrations.AddField(
            model_name='posts',
            name='likes',
            field=models.ManyToManyField(related_name='likes', to=settings.AUTH_USER_MODEL),
        ),
        migrations.DeleteModel(
            name='Likes',
        ),
    ]
