# -*- coding: utf-8 -*-

from django.core.serializers.python import Serializer
from .models import Exercises, Categories, Repeats

class ExercisesSerializer(Serializer):
    def end_object(self, obj):
        self._current['exercise_id'] = obj.id
        self._current['category_name'] = str(Categories.objects.get(pk=self._current['category']))
        self.objects.append(self._current)


class SetsByDateSerializer(Serializer):
    def end_object(self, obj):
        repeats = list()
        sets = dict()
        r = Repeats.objects.filter(set=obj.id)
        exercise = Exercises.objects.get(id=obj.exercise.id)
        for rep in r:
            repeats.append({'weight': rep.weight, 'repeats': rep.repeats, 'repeat_id': rep.id})
            # repeats[rep.weight] = rep.repeats
            # repeats[rep.id] = {rep.weight: rep.repeats}
        sets['exercise_name'] = exercise.name
        sets['category_id'] = exercise.category.id
        sets['category_name'] = exercise.category.name
        sets['repeats'] = repeats
        self._current['date'] = obj.date.strftime("%Y-%m-%d")
        self._current['user'] = obj.user.id
        self._current['items'] = sets
        self._current['set_id'] = obj.id
        self.objects.append(self._current)


class RepeatsSerializer(Serializer):
    def end_object(self, obj):
        self._current['weight'] = obj.weight
        self._current['repeats'] = obj.repeats
        self._current['set'] = obj.set.id
        self.objects.append(self._current)


class CategoriesSerializer(Serializer):
    def end_object(self, obj):
        self._current['category_id'] = obj.id
        self.objects.append(self._current)


class ProfileSerializer(Serializer):
    def end_object(self, obj):
        del self._current['last_login']
        self._current['date_joined'] = obj.date_joined.strftime("%Y-%m-%d")
        del self._current['is_active']
        del self._current['is_superuser']
        del self._current['is_staff']
        del self._current['groups']
        del self._current['user_permissions']
        del self._current['password']
        self.objects.append(self._current)


class BodySizeSerializer(Serializer):
    def end_object(self, obj):
        self._current['id'] = obj.id
        self._current['date'] = obj.date.strftime("%Y-%m-%d")
        self.objects.append(self._current)