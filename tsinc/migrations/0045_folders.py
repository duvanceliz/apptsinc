# Generated by Django 5.0.6 on 2024-06-16 15:22

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('tsinc', '0044_panelitems_name'),
    ]

    operations = [
        migrations.CreateModel(
            name='Folders',
            fields=[
                ('id', models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('name', models.CharField(default=None, max_length=100)),
                ('path', models.CharField(default=None, max_length=200)),
            ],
        ),
    ]