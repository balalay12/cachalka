# -*- coding: utf-8 -*-
import json

from django.core.serializers.python import Serializer
from django.core.serializers.json import DjangoJSONEncoder
from datetime import datetime
from .models import Exercises, Categories, Sets, Repeats

class ExercisesSerializer(Serializer):
    def end_object(self, obj):
        self._current['exercise_id'] = obj.id
        self._current['category_name'] = str(Categories.objects.get(pk=self._current['category']))
        self.objects.append(self._current)


class SetsByDateSerializer(Serializer):
    def end_object(self, obj):
        repeats = {}
        sets = {}
        repeat = {}
        r = Repeats.objects.filter(set=obj.id)
        for rep in r:
            repeats[rep.weight] = rep.repeats
            # repeats[rep.id] = {rep.weight: rep.repeats}
        sets['exercise_name'] = str(Exercises.objects.get(id=obj.exercise.id))
        sets['repeats'] = repeats
        self._current['date'] = obj.date.strftime("%Y-%m-%d")
        self._current['user'] = obj.user.id
        self._current['items'] = sets
        self._current['set_id'] = obj.id
        self.objects.append(self._current)


class CategoriesSerializer(Serializer):
    def end_object(self, obj):
        self._current['category_id'] = obj.id
        self.objects.append(self._current)
