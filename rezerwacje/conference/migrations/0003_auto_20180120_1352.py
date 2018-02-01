# -*- coding: utf-8 -*-
# Generated by Django 1.11.4 on 2018-01-20 13:52
from __future__ import unicode_literals

from django.db import migrations, models
import django.db.models.deletion


class Migration(migrations.Migration):

    dependencies = [
        ('conference', '0002_auto_20180120_1350'),
    ]

    operations = [
        migrations.AlterField(
            model_name='booking',
            name='comment',
            field=models.TextField(blank=True, default=''),
        ),
        migrations.AlterField(
            model_name='booking',
            name='date',
            field=models.DateField(auto_now_add=True),
        ),
        migrations.AlterField(
            model_name='booking',
            name='room',
            field=models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, related_name='bookings', to='conference.Room'),
        ),
    ]