# Generated by Django 5.0.6 on 2024-08-16 16:49

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('tsinc', '0065_trm'),
    ]

    operations = [
        migrations.AlterField(
            model_name='trm',
            name='value',
            field=models.FloatField(default=0),
        ),
    ]
