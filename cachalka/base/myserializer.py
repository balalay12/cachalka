# -*- coding: utf-8 -*-

from django.core.serializers.python import Serializer
from .models import Exercises, Categories

class ExercisesSerializer(Serializer):
    def end_object(self, obj):
        self._current['category_name'] = str(Categories.objects.get(pk=self._current['category']))
        self.objects.append(self._current)
