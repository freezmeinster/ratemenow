# -*- coding: utf-8 -*-
from __future__ import unicode_literals

from django.contrib import admin
from .models import UserRate

class UserRateAdmin(admin.ModelAdmin):
    list_display = ['user', 'place', 'rate_star', 'rate_comment', 'created_date']

admin.site.register(UserRate, UserRateAdmin)
