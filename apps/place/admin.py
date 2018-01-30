# -*- coding: utf-8 -*-
from __future__ import unicode_literals

from django.contrib import admin
from .models import (Place, PlaceCategory, Tag, University, Faculty,
    StudyProgram, EducationPlace)

def activate_place(modeladmin, request, queryset):
    for query in queryset :
        query.activate()
activate_place.short_description = "Activate Place"


class PlaceAdmin(admin.ModelAdmin):
    list_display = ['name', 'owner', 'category', 'is_active', 'total_rate', 'total_user']
    readonly_fields = ['is_active', ]
    actions = [activate_place, ]

admin.site.register(Place, PlaceAdmin)
admin.site.register(PlaceCategory)
admin.site.register(Tag)
admin.site.register(University)
admin.site.register(Faculty)
admin.site.register(StudyProgram)
admin.site.register(EducationPlace)
