# -*- coding: utf-8 -*-
from __future__ import unicode_literals

from django.db import models, migrations


class Migration(migrations.Migration):

    dependencies = [
        ('base', '0001_initial'),
    ]

    operations = [
        migrations.RemoveField(
            model_name='sets',
            name='created',
        ),
        migrations.RemoveField(
            model_name='sets',
            name='modified',
        ),
        migrations.AddField(
            model_name='sets',
            name='date',
            field=models.DateField(default=None),
        ),
    ]
