# Generated by Django 5.0.6 on 2024-07-26 19:41

from django.db import migrations


class Migration(migrations.Migration):

    dependencies = [
        ('tsinc', '0040_remove_orderentry_leftover_orderentry_tracking'),
    ]

    operations = [
        migrations.RenameField(
            model_name='orderentry',
            old_name='Tracking',
            new_name='tracking',
        ),
    ]
