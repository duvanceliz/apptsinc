# Generated by Django 5.0.6 on 2024-07-16 13:37

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('tsinc', '0022_alter_product_description'),
    ]

    operations = [
        migrations.AddField(
            model_name='project',
            name='nit',
            field=models.CharField(max_length=200, null=True),
        ),
    ]