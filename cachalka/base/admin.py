from django.contrib import admin
from .models import Exercises, Categories, Sets, Repeats

admin.site.register(Exercises)
admin.site.register(Categories)
admin.site.register(Sets)
admin.site.register(Repeats)


class ExercisesAdmin(admin.ModelAdmin):
    fields = ('name', 'category',)


class CategoriesAdmin(admin.ModelAdmin):
    fields = ('name',)


class SetsAdmin(admin.ModelAdmin):
    fields = ('date', 'exercise', 'user',)


class RepeatsAdmin(admin.ModelAdmin):
    fields = ('set', 'weight', 'repeats')

