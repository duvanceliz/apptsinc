# Generated by Django 5.0.6 on 2024-08-02 17:30

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('tsinc', '0053_remove_orderentry_price_u_remove_productsent_price_u'),
    ]

    operations = [
        migrations.AddField(
            model_name='product',
            name='min_stock',
            field=models.IntegerField(default=0),
        ),
    ]
