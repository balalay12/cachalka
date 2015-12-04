# -*- coding: utf-8 -*-
from __future__ import unicode_literals

from django.db import models, migrations


class Migration(migrations.Migration):

    dependencies = [
        ('base', '0002_auto_20151130_2029'),
    ]

    operations = [
        migrations.AlterField(
            model_name='repeats',
            name='weight',
            field=models.FloatField(verbose_name='\u0412\u0435\u0441'),
        ),
    ]
