# Generated by Django 5.0.6 on 2024-07-06 16:19

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('tsinc', '0004_tabs_chest_type'),
    ]

    operations = [
        migrations.CreateModel(
            name='License',
            fields=[
                ('id', models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('ref', models.CharField(default=None, max_length=100)),
                ('description', models.CharField(default=None, max_length=200)),
            ],
        ),
    ]