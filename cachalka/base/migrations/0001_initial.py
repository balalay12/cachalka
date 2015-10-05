# -*- coding: utf-8 -*-
from __future__ import unicode_literals

from django.db import models, migrations
import django.utils.timezone
from django.conf import settings
import model_utils.fields


class Migration(migrations.Migration):

    dependencies = [
        migrations.swappable_dependency(settings.AUTH_USER_MODEL),
    ]

    operations = [
        migrations.CreateModel(
            name='Categories',
            fields=[
                ('id', models.AutoField(verbose_name='ID', serialize=False, auto_created=True, primary_key=True)),
                ('name', models.CharField(max_length=255)),
            ],
            options={
                'verbose_name': '\u043a\u0430\u0442\u0435\u0433\u043e\u0440\u0438\u044f',
                'verbose_name_plural': '\u043a\u0430\u0442\u0435\u0433\u043e\u0440\u0438\u0438',
            },
        ),
        migrations.CreateModel(
            name='Exercises',
            fields=[
                ('id', models.AutoField(verbose_name='ID', serialize=False, auto_created=True, primary_key=True)),
                ('name', models.CharField(max_length=255)),
                ('category', models.ForeignKey(to='base.Categories')),
            ],
            options={
                'verbose_name': '\u0443\u043f\u0440\u0430\u0436\u043d\u0435\u043d\u0438\u0435',
                'verbose_name_plural': '\u0443\u043f\u0440\u0430\u0436\u043d\u0435\u043d\u0438\u044f',
            },
        ),
        migrations.CreateModel(
            name='Repeats',
            fields=[
                ('id', models.AutoField(verbose_name='ID', serialize=False, auto_created=True, primary_key=True)),
                ('weight', models.IntegerField(verbose_name='\u0412\u0435\u0441')),
                ('repeats', models.IntegerField(verbose_name='\u041f\u043e\u0432\u0442\u043e\u0440\u044b')),
            ],
            options={
                'verbose_name': '\u043f\u043e\u0432\u0442\u043e\u0440\u0435\u043d\u0438\u0435',
                'verbose_name_plural': '\u043f\u043e\u0432\u0442\u043e\u0440\u044b',
            },
        ),
        migrations.CreateModel(
            name='Sets',
            fields=[
                ('id', models.AutoField(verbose_name='ID', serialize=False, auto_created=True, primary_key=True)),
                ('created', model_utils.fields.AutoCreatedField(default=django.utils.timezone.now, verbose_name='created', editable=False)),
                ('modified', model_utils.fields.AutoLastModifiedField(default=django.utils.timezone.now, verbose_name='modified', editable=False)),
                ('exercise', models.ForeignKey(to='base.Exercises')),
                ('user', models.ForeignKey(to=settings.AUTH_USER_MODEL)),
            ],
            options={
                'verbose_name': '\u043f\u043e\u0434\u0445\u043e\u0434',
                'verbose_name_plural': '\u043f\u043e\u0434\u0445\u043e\u0434\u044b',
            },
        ),
        migrations.AddField(
            model_name='repeats',
            name='set',
            field=models.ForeignKey(default=None, to='base.Sets'),
        ),
    ]
