# Generated by Django 5.0.6 on 2024-08-03 15:18

import django.db.models.deletion
from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('tsinc', '0054_product_min_stock'),
    ]

    operations = [
        migrations.CreateModel(
            name='ProductStatictics',
            fields=[
                ('id', models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('rotations', models.IntegerField(default=0)),
                ('out_stock', models.FloatField(default=0)),
                ('product', models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, to='tsinc.orderproduct')),
            ],
        ),
    ]
