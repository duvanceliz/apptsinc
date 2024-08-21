# Generated by Django 5.0.6 on 2024-08-15 20:30

import django.core.validators
from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('tsinc', '0059_product_observation'),
    ]

    operations = [
        migrations.AlterField(
            model_name='product',
            name='observation',
            field=models.TextField(null=True, validators=[django.core.validators.MaxLengthValidator(200)]),
        ),
    ]