# Generated by Django 5.0.6 on 2024-08-02 15:42

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('tsinc', '0050_orderentry_price'),
    ]

    operations = [
        migrations.AddField(
            model_name='productsent',
            name='price',
            field=models.FloatField(default=0),
        ),
    ]
