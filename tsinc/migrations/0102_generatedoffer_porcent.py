# Generated by Django 5.0.6 on 2024-09-06 19:55

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('tsinc', '0101_alter_generatedoffer_measure_and_more'),
    ]

    operations = [
        migrations.AddField(
            model_name='generatedoffer',
            name='porcent',
            field=models.FloatField(blank=True, default=0, null=True),
        ),
    ]
