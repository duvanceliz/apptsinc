# Generated by Django 5.0.6 on 2024-05-29 19:36

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('tsinc', '0020_items_zindex'),
    ]

    operations = [
        migrations.AddField(
            model_name='items',
            name='height',
            field=models.FloatField(default=0),
        ),
        migrations.AddField(
            model_name='items',
            name='width',
            field=models.FloatField(default=0),
        ),
    ]