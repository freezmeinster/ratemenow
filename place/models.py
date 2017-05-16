# -*- coding: utf-8 -*-
from __future__ import unicode_literals

from django.db import models
from django.contrib.auth.models import User

# import ini digunakan untuk memanggil fungsi Sum
from django.db.models import Sum

class Place(models.Model):
    name = models.CharField(max_length=255)
    description = models.TextField()
    picture = models.ImageField(upload_to="assets/place_picture")
    is_active = models.BooleanField(default=False)
    owner = models.ForeignKey(User)
    
    def __unicode__(self):
        return self.name
    
    @property
    def total_rate(self):
        total = self.userrate_set.all().aggregate(Sum('rate_star'))
        return total.get("rate_star__sum")
    
    @property
    def total_user(self):
        total = self.userrate_set.all().count()
        return total
    
    def activate(self):
        if self.is_active :
            self.is_active = False
        else :
             self.is_active = True
        self.save()