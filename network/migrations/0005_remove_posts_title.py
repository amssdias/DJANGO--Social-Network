# Generated by Django 3.0.8 on 2020-10-13 23:27

from django.db import migrations


class Migration(migrations.Migration):

    dependencies = [
        ('network', '0004_auto_20201012_0249'),
    ]

    operations = [
        migrations.RemoveField(
            model_name='posts',
            name='title',
        ),
    ]
