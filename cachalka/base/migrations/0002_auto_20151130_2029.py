# -*- coding: utf-8 -*-
from __future__ import unicode_literals

from django.db import models, migrations
from django.conf import settings


class Migration(migrations.Migration):

    dependencies = [
        migrations.swappable_dependency(settings.AUTH_USER_MODEL),
        ('base', '0001_initial'),
    ]

    operations = [
        migrations.CreateModel(
            name='BodySize',
            fields=[
                ('id', models.AutoField(verbose_name='ID', serialize=False, auto_created=True, primary_key=True)),
                ('date', models.DateField(default=None, verbose_name='\u0414\u0430\u0442\u0430 \u0437\u0430\u043c\u0435\u0440\u043e\u0432')),
                ('chest', models.FloatField(verbose_name='\u0413\u0440\u0443\u0434\u044c')),
                ('waist', models.FloatField(verbose_name='\u0422\u0430\u043b\u0438\u044f')),
                ('hip', models.FloatField(verbose_name='\u0411\u0435\u0434\u0440\u0430')),
                ('arm', models.FloatField(verbose_name='\u0420\u0443\u043a\u0438')),
                ('weight', models.FloatField(verbose_name='\u0412\u0435\u0441')),
                ('user', models.ForeignKey(to=settings.AUTH_USER_MODEL)),
            ],
            options={
                'verbose_name': '\u0417\u0430\u043c\u0435\u0440\u044b \u0442\u0435\u043b\u0430',
                'verbose_name_plural': '\u0417\u0430\u043c\u0435\u0440\u044b \u0442\u0435\u043b\u0430',
            },
        ),
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
