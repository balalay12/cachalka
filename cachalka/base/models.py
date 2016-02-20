# -*- coding: utf-8 -*-

from django.db import models
from django.contrib.auth.models import AbstractUser
from django.conf import settings


class Categories(models.Model):
    name = models.CharField(max_length=255)

    def __unicode__(self):
        return u'%s' % self.name

    class Meta:
        verbose_name = u'категория'
        verbose_name_plural = u'категории'


class Exercises(models.Model):
    name = models.CharField(max_length=255)
    category = models.ForeignKey(Categories)

    def __unicode__(self):
        return u'%s' % self.name

    class Meta:
        verbose_name = u'упражнение'
        verbose_name_plural = u'упражнения'


class Sets(models.Model):
    date = models.DateField(default=None)
    user = models.ForeignKey(settings.AUTH_USER_MODEL)
    exercise = models.ForeignKey(Exercises)
    # repeats = models.ForeignKey(Repeats, default=None)

    class Meta:
        verbose_name = u'подход'
        verbose_name_plural = u'подходы'


class Repeats(models.Model):
    set = models.ForeignKey(Sets, default=None)
    weight = models.FloatField(verbose_name=u"Вес")
    repeats = models.IntegerField(verbose_name=u'Повторы')

    class Meta:
        verbose_name = u'повторение'
        verbose_name_plural = u'повторы'


class BodySize(models.Model):
    date = models.DateField(default=None, verbose_name=u'Дата замеров')
    chest = models.FloatField(verbose_name=u'Грудь', blank=True, null=True)
    waist = models.FloatField(verbose_name=u'Талия', blank=True, null=True)
    hip = models.FloatField(verbose_name=u'Бедра', blank=True, null=True)
    arm = models.FloatField(verbose_name=u'Руки', blank=True, null=True)
    weight = models.FloatField(verbose_name=u'Вес', blank=True, null=True)
    user = models.ForeignKey(settings.AUTH_USER_MODEL)

    class Meta:
        verbose_name = u'Замеры тела'
        verbose_name_plural = u'Замеры тела'


class MyUser(AbstractUser):
    height = models.IntegerField(verbose_name=u'Рост', blank=True, null=True)

