# -*- coding: utf-8 -*-
from __future__ import unicode_literals

from django.db import models, migrations


class Migration(migrations.Migration):

    dependencies = [
        ('base', '0004_auto_20151209_2044'),
    ]

    operations = [
        migrations.AlterField(
            model_name='bodysize',
            name='arm',
            field=models.FloatField(null=True, verbose_name='\u0420\u0443\u043a\u0438', blank=True),
        ),
        migrations.AlterField(
            model_name='bodysize',
            name='chest',
            field=models.FloatField(null=True, verbose_name='\u0413\u0440\u0443\u0434\u044c', blank=True),
        ),
        migrations.AlterField(
            model_name='bodysize',
            name='hip',
            field=models.FloatField(null=True, verbose_name='\u0411\u0435\u0434\u0440\u0430', blank=True),
        ),
        migrations.AlterField(
            model_name='bodysize',
            name='waist',
            field=models.FloatField(null=True, verbose_name='\u0422\u0430\u043b\u0438\u044f', blank=True),
        ),
        migrations.AlterField(
            model_name='bodysize',
            name='weight',
            field=models.FloatField(null=True, verbose_name='\u0412\u0435\u0441', blank=True),
        ),
    ]
