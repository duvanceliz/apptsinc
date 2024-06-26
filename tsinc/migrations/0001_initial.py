# Generated by Django 5.0.6 on 2024-06-19 17:00

import datetime
import django.db.models.deletion
from django.conf import settings
from django.db import migrations, models


class Migration(migrations.Migration):

    initial = True

    dependencies = [
        migrations.swappable_dependency(settings.AUTH_USER_MODEL),
    ]

    operations = [
        migrations.CreateModel(
            name='Brand',
            fields=[
                ('id', models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('product_brand', models.CharField(default=None, max_length=200)),
            ],
        ),
        migrations.CreateModel(
            name='Category',
            fields=[
                ('id', models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('name', models.CharField(default=None, max_length=100)),
            ],
        ),
        migrations.CreateModel(
            name='Dasboard',
            fields=[
                ('id', models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('name', models.CharField(default=None, max_length=200)),
                ('quantity', models.IntegerField(default=0)),
            ],
        ),
        migrations.CreateModel(
            name='Folders',
            fields=[
                ('id', models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('name', models.CharField(default=None, max_length=100)),
                ('path', models.CharField(default=None, max_length=200)),
            ],
        ),
        migrations.CreateModel(
            name='Location',
            fields=[
                ('id', models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('product_location', models.CharField(default=None, max_length=200)),
            ],
        ),
        migrations.CreateModel(
            name='Product',
            fields=[
                ('id', models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('code', models.CharField(default=None, max_length=200)),
                ('product_name', models.CharField(default=None, max_length=200)),
                ('factory_ref', models.CharField(default=None, max_length=200)),
                ('model', models.CharField(default=None, max_length=200)),
                ('sale_price', models.FloatField(default=0)),
                ('brand', models.CharField(default=None, max_length=200)),
                ('location', models.CharField(default=None, max_length=200)),
                ('quantity', models.IntegerField()),
                ('point', models.CharField(blank=True, max_length=100, null=True)),
                ('description', models.CharField(blank=True, max_length=200, null=True)),
                ('iva', models.BooleanField(default=False)),
                ('date', models.DateField(default=datetime.date.today)),
            ],
        ),
        migrations.CreateModel(
            name='Labels',
            fields=[
                ('id', models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('id_code', models.CharField(default=None, max_length=50)),
                ('value', models.CharField(default=None, max_length=200)),
                ('x', models.FloatField()),
                ('y', models.FloatField()),
                ('zindex', models.IntegerField(default=0)),
                ('width', models.FloatField(default=0)),
                ('height', models.FloatField(default=0)),
                ('relationship', models.CharField(max_length=50, null=True)),
                ('dashboard', models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, related_name='labels', to='tsinc.dasboard')),
            ],
        ),
        migrations.CreateModel(
            name='PanelItems',
            fields=[
                ('id', models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('name', models.CharField(max_length=100, null=True)),
                ('img', models.CharField(default=None, max_length=100)),
                ('tag', models.CharField(max_length=100, null=True)),
                ('folder', models.ForeignKey(null=True, on_delete=django.db.models.deletion.CASCADE, related_name='panelitems', to='tsinc.folders')),
                ('product', models.ForeignKey(blank=True, null=True, on_delete=django.db.models.deletion.SET_NULL, related_name='items', to='tsinc.product')),
            ],
        ),
        migrations.CreateModel(
            name='Items',
            fields=[
                ('id', models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('id_code', models.CharField(default=None, max_length=50)),
                ('x', models.FloatField()),
                ('y', models.FloatField()),
                ('zindex', models.IntegerField(default=0)),
                ('width', models.FloatField(default=0)),
                ('height', models.FloatField(default=0)),
                ('relationship', models.CharField(max_length=50, null=True)),
                ('dashboard', models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, related_name='dashboard', to='tsinc.dasboard')),
                ('img', models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, related_name='panelitem', to='tsinc.panelitems')),
            ],
        ),
        migrations.CreateModel(
            name='Project',
            fields=[
                ('id', models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('name', models.CharField(default=None, max_length=200)),
                ('company_name', models.CharField(default=None, max_length=200)),
                ('asesor', models.CharField(default=None, max_length=200)),
                ('controller', models.CharField(blank=True, max_length=100, null=True)),
                ('verified', models.BooleanField(default=False)),
                ('progress', models.IntegerField(default=0)),
                ('date', models.DateField(default=datetime.date.today)),
                ('usersesion', models.ForeignKey(default=None, on_delete=django.db.models.deletion.CASCADE, to=settings.AUTH_USER_MODEL)),
            ],
        ),
        migrations.CreateModel(
            name='Subcategory',
            fields=[
                ('id', models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('name', models.CharField(default=None, max_length=100)),
                ('tag', models.CharField(default=None, max_length=100)),
                ('category', models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, related_name='subcategory', to='tsinc.category')),
            ],
        ),
        migrations.CreateModel(
            name='Tabs',
            fields=[
                ('id', models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('tab_name', models.CharField(default=None, max_length=200)),
                ('controller', models.CharField(max_length=100, null=True)),
                ('project', models.ForeignKey(blank=True, null=True, on_delete=django.db.models.deletion.CASCADE, related_name='tabs', to='tsinc.project')),
            ],
        ),
        migrations.AddField(
            model_name='dasboard',
            name='tab',
            field=models.ForeignKey(blank=True, null=True, on_delete=django.db.models.deletion.CASCADE, related_name='dashboards', to='tsinc.tabs'),
        ),
    ]
