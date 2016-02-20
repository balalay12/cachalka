# -*- coding: utf-8 -*-
from __future__ import unicode_literals

from django.db import models, migrations
import django.contrib.auth.models
import django.utils.timezone
from django.conf import settings
import django.core.validators


class Migration(migrations.Migration):

    dependencies = [
        ('auth', '0006_require_contenttypes_0002'),
    ]

    operations = [
        migrations.CreateModel(
            name='MyUser',
            fields=[
                ('id', models.AutoField(verbose_name='ID', serialize=False, auto_created=True, primary_key=True)),
                ('password', models.CharField(max_length=128, verbose_name='password')),
                ('last_login', models.DateTimeField(null=True, verbose_name='last login', blank=True)),
                ('is_superuser', models.BooleanField(default=False, help_text='Designates that this user has all permissions without explicitly assigning them.', verbose_name='superuser status')),
                ('username', models.CharField(error_messages={'unique': 'A user with that username already exists.'}, max_length=30, validators=[django.core.validators.RegexValidator('^[\\w.@+-]+$', 'Enter a valid username. This value may contain only letters, numbers and @/./+/-/_ characters.', 'invalid')], help_text='Required. 30 characters or fewer. Letters, digits and @/./+/-/_ only.', unique=True, verbose_name='username')),
                ('first_name', models.CharField(max_length=30, verbose_name='first name', blank=True)),
                ('last_name', models.CharField(max_length=30, verbose_name='last name', blank=True)),
                ('email', models.EmailField(max_length=254, verbose_name='email address', blank=True)),
                ('is_staff', models.BooleanField(default=False, help_text='Designates whether the user can log into this admin site.', verbose_name='staff status')),
                ('is_active', models.BooleanField(default=True, help_text='Designates whether this user should be treated as active. Unselect this instead of deleting accounts.', verbose_name='active')),
                ('date_joined', models.DateTimeField(default=django.utils.timezone.now, verbose_name='date joined')),
                ('height', models.IntegerField(verbose_name='\u0420\u043e\u0441\u0442', blank=True)),
                ('groups', models.ManyToManyField(related_query_name='user', related_name='user_set', to='auth.Group', blank=True, help_text='The groups this user belongs to. A user will get all permissions granted to each of their groups.', verbose_name='groups')),
                ('user_permissions', models.ManyToManyField(related_query_name='user', related_name='user_set', to='auth.Permission', blank=True, help_text='Specific permissions for this user.', verbose_name='user permissions')),
            ],
            options={
                'abstract': False,
                'verbose_name': 'user',
                'verbose_name_plural': 'users',
            },
            managers=[
                ('objects', django.contrib.auth.models.UserManager()),
            ],
        ),
        migrations.CreateModel(
            name='BodySize',
            fields=[
                ('id', models.AutoField(verbose_name='ID', serialize=False, auto_created=True, primary_key=True)),
                ('date', models.DateField(default=None, verbose_name='\u0414\u0430\u0442\u0430 \u0437\u0430\u043c\u0435\u0440\u043e\u0432')),
                ('chest', models.FloatField(null=True, verbose_name='\u0413\u0440\u0443\u0434\u044c', blank=True)),
                ('waist', models.FloatField(null=True, verbose_name='\u0422\u0430\u043b\u0438\u044f', blank=True)),
                ('hip', models.FloatField(null=True, verbose_name='\u0411\u0435\u0434\u0440\u0430', blank=True)),
                ('arm', models.FloatField(null=True, verbose_name='\u0420\u0443\u043a\u0438', blank=True)),
                ('weight', models.FloatField(null=True, verbose_name='\u0412\u0435\u0441', blank=True)),
                ('user', models.ForeignKey(to=settings.AUTH_USER_MODEL)),
            ],
            options={
                'verbose_name': '\u0417\u0430\u043c\u0435\u0440\u044b \u0442\u0435\u043b\u0430',
                'verbose_name_plural': '\u0417\u0430\u043c\u0435\u0440\u044b \u0442\u0435\u043b\u0430',
            },
        ),
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
                ('weight', models.FloatField(verbose_name='\u0412\u0435\u0441')),
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
                ('date', models.DateField(default=None)),
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
