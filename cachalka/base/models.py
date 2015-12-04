# -*- coding: utf-8 -*-

from django.db import models


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
    user = models.ForeignKey('auth.User')
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
    chest = models.FloatField(verbose_name=u'Грудь')
    waist = models.FloatField(verbose_name=u'Талия')
    hip = models.FloatField(verbose_name=u'Бедра')
    arm = models.FloatField(verbose_name=u'Руки')
    weight = models.FloatField(verbose_name=u'Вес')
    user = models.ForeignKey('auth.User')

    class Meta:
        verbose_name = u'Замеры тела'
        verbose_name_plural = u'Замеры тела'
