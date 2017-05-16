# -*- coding: utf-8 -*-
from __future__ import unicode_literals

from django.contrib import admin
from .models import Place

def activate_place(modeladmin, request, queryset):
    for query in queryset :
        query.activate()
activate_place.short_description = "Activate Place"


class PlaceAdmin(admin.ModelAdmin):
    list_display = ['name', 'owner', 'is_active', 'total_rate', 'total_user']
    readonly_fields = ['is_active', ]
    actions = [activate_place, ]

admin.site.register(Place, PlaceAdmin)