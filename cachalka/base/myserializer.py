# -*- coding: utf-8 -*-
import json

from django.core.serializers.python import Serializer
from django.core.serializers.json import DjangoJSONEncoder
from datetime import datetime
from .models import Exercises, Categories, Sets, Repeats

class ExercisesSerializer(Serializer):
    def end_object(self, obj):
        self._current['category_name'] = str(Categories.objects.get(pk=self._current['category']))
        self.objects.append(self._current)


class SetSerializer(Serializer):
    def end_object(self, obj):
        repeats = {}
        r = Repeats.objects.filter(set=obj.id)
        for rep in r:
            repeats[rep.weight] = rep.repeats
        # exercise = Exercises.objects.get(id=int(obj.exercise))
        # print obj.exercise.id
        self._current['exercise_name'] = str(Exercises.objects.get(id=obj.exercise.id))
        self._current['created'] = json.dumps(obj.created, cls=DjangoJSONEncoder)
        self._current['modified'] = json.dumps(obj.modified, cls=DjangoJSONEncoder)
        self._current['repeats'] = repeats
        self.objects.append(self._current)


class SetsByDateSerializer(Serializer):
    def end_object(self, obj):
        repeats = {}
        sets = {}
        t = {}
        r = Repeats.objects.filter(set=obj.id)
        for rep in r:
            repeats[rep.weight] = rep.repeats
        sets['exercise_name'] = str(Exercises.objects.get(id=obj.exercise.id))
        sets['repeats'] = repeats
        t[json.dumps(obj.created, cls=DjangoJSONEncoder)] = sets
        self._current['created'] = json.dumps(obj.created, cls=DjangoJSONEncoder)
        self._current['modified'] = json.dumps(obj.modified, cls=DjangoJSONEncoder)
        self._current['sets'] = t
        self.objects.append(self._current)
