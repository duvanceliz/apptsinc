# Generated by Django 5.0.6 on 2024-08-01 15:44

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('tsinc', '0048_remission_number_remission_order_number_and_more'),
    ]

    operations = [
        migrations.AddField(
            model_name='productsent',
            name='discounted',
            field=models.BooleanField(default=False),
        ),
    ]
