# Generated by Django 4.1.7 on 2023-04-02 18:19

import django.contrib.gis.db.models.fields
from django.db import migrations


class Migration(migrations.Migration):

    dependencies = [
        ('app', '0004_alter_restaurant_owner'),
    ]

    operations = [
        migrations.AddField(
            model_name='restaurant',
            name='location',
            field=django.contrib.gis.db.models.fields.PointField(blank=True, null=True, srid=4326),
        ),
    ]
