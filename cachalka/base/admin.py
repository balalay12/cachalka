from django.contrib import admin
from .models import Exercises, Categories, Sets, Repeats


class ExercisesAdmin(admin.ModelAdmin):
    fields = ('name', 'category',)
    list_display = ('name', 'category')


class CategoriesAdmin(admin.ModelAdmin):
    fields = ('name',)
    list_display = ('name',)


class SetsAdmin(admin.ModelAdmin):
    fields = ('date', 'exercise', 'user',)
    list_display = ('date', 'user', 'exercise')


class RepeatsAdmin(admin.ModelAdmin):
    fields = ('set', 'weight', 'repeats')
    list_display = ('set', 'weight', 'repeats')

admin.site.register(Exercises, ExercisesAdmin)
admin.site.register(Categories, CategoriesAdmin)
admin.site.register(Sets, SetsAdmin)
admin.site.register(Repeats, RepeatsAdmin)