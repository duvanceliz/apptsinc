# Generated by Django 5.0.6 on 2024-07-24 14:43

import django.db.models.deletion
from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('tsinc', '0035_orderentry'),
    ]

    operations = [
        migrations.AlterField(
            model_name='orderentry',
            name='product',
            field=models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, to='tsinc.orderproduct'),
        ),
    ]
