# -*- coding: utf-8 -*-

from django.db import models
from model_utils.models import TimeStampedModel

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


class Sets(TimeStampedModel):
    user = models.ForeignKey('auth.User')
    exercise = models.ForeignKey(Exercises)

    class Meta:
        verbose_name = u'подход'
        verbose_name_plural = u'подходы'


class Repeats(models.Model):
    set = models.ManyToManyField(Sets)
    weight = models.IntegerField(verbose_name=u"Вес")
    repeats = models.IntegerField(verbose_name=u'Повторы')

    class Meta:
        verbose_name = u'повторение'
        verbose_name_plural = u'повторы'
