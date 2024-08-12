# Generated by Django 5.0.6 on 2024-07-04 16:39

import django.db.models.deletion
from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('tsinc', '0002_items_tag'),
    ]

    operations = [
        migrations.CreateModel(
            name='Sheet',
            fields=[
                ('id', models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('name', models.CharField(default=None, max_length=100)),
                ('project', models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, related_name='sheet', to='tsinc.project')),
            ],
        ),
        migrations.CreateModel(
            name='Points',
            fields=[
                ('id', models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('name', models.CharField(default=None, max_length=100)),
                ('eu', models.IntegerField(default=0)),
                ('ed', models.IntegerField(default=0)),
                ('sa', models.IntegerField(default=0)),
                ('sd', models.IntegerField(default=0)),
                ('sc', models.IntegerField(default=0)),
                ('sheet', models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, related_name='point', to='tsinc.sheet')),
            ],
        ),
    ]