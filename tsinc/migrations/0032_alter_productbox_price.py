# Generated by Django 5.0.6 on 2024-07-19 21:40

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('tsinc', '0031_purcharseorder_usersession'),
    ]

    operations = [
        migrations.AlterField(
            model_name='productbox',
            name='price',
            field=models.FloatField(default=0),
        ),
    ]
