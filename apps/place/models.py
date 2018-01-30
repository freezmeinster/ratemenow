# -*- coding: utf-8 -*-
from __future__ import unicode_literals

from django.db import models
from django.contrib.auth.models import User
from django.contrib.contenttypes.models import ContentType
from django.conf import settings
from django.contrib.postgres.fields import ArrayField

# import ini digunakan untuk memanggil fungsi Sum
from django.db.models import Sum

# Place Category
class PlaceCategory(models.Model):
    name = models.CharField(max_length=255)
    description = models.TextField()

    def __unicode__(self):
        return self.name

    def __str__(self):
        return self.name

# Tag
class Tag(models.Model):
    name = models.CharField(max_length=255)
    description = models.TextField()

    def __unicode__(self):
        return self.name

    def __str__(self):
        return self.name

# Place
class Place(models.Model):
    name = models.CharField(max_length=255)
    description = models.TextField()
    picture = models.ImageField(upload_to="assets/picture/place")
    is_active = models.BooleanField(default=False)
    owner = models.ForeignKey(User)
    category = models.ForeignKey(PlaceCategory)
    tags = models.ManyToManyField("tag", symmetrical=False, related_name="place_tags", blank=True)

    def __unicode__(self):
        return self.name

    def __str__(self):
        return self.name

    @property
    def total_rate(self):
        total = self.userrate_set.all().aggregate(Sum('rate_star'))
        return total.get("rate_star__sum") or 0

    @property
    def total_user(self):
        total = self.userrate_set.all().count()
        return total

    @property
    def get_picture_url(self):
        img_url = "{0}{1}".format('/', self.picture.url.strip("assets/picture/place"))
        return img_url

    def activate(self):
        if self.is_active :
            self.is_active = False
        else :
             self.is_active = True
        self.save()

# University
class University(models.Model):
    name = models.CharField(max_length=255)
    description = models.TextField()
    address = models.TextField()
    picture = models.ImageField(upload_to="assets/picture/university")
    is_active = models.BooleanField(default=False)
    owner = models.ForeignKey(User)
    tags = models.ManyToManyField("tag", symmetrical=False, related_name="university_tags", blank=True)

    def __unicode__(self):
        return self.name

    def __str__(self):
        return self.name

    @property
    def get_picture_url(self):
        base_static_url = settings.STATIC_URL
        img_url = "{0}{1}".format(base_static_url, self.picture.url.strip("assets/picture/university"))
        return img_url

    def activate(self):
        if self.is_active :
            self.is_active = False
        else :
             self.is_active = True
        self.save()

# Faculty
class Faculty(models.Model):
    name = models.CharField(max_length=255)
    description = models.TextField()
    tags = models.ManyToManyField("tag", symmetrical=False, related_name="faculty_tags", blank=True)

    def __unicode__(self):
        return self.name

    def __str__(self):
        return self.name

# Study Program
class StudyProgram(models.Model):
    name = models.CharField(max_length=255)
    description = models.TextField()
    tags = models.ManyToManyField("tag", symmetrical=False, related_name="studyprogram_tags", blank=True)

    def __unicode__(self):
        return self.name

    def __str__(self):
        return self.name

# Education Place
class EducationPlace(models.Model):
    name = models.CharField(max_length=255)
    description = models.TextField()
    picture = models.ImageField(upload_to="assets/picture/eduplace")
    is_active = models.BooleanField(default=False)
    university = models.ForeignKey(University)
    faculty = models.ForeignKey(Faculty)
    studyprogram = models.ForeignKey(StudyProgram)
    category = models.ForeignKey(PlaceCategory)
    tags = models.ManyToManyField("tag", symmetrical=False, related_name="education_place_tags", blank=True)

    def __unicode__(self):
        return self.name

    def __str__(self):
        return self.name

    @property
    def get_picture_url(self):
        base_static_url = settings.STATIC_URL
        img_url = "{0}{1}".format(base_static_url, self.picture.url.strip("assets/picture/eduplace"))
        return img_url

    def activate(self):
        if self.is_active :
            self.is_active = False
        else :
             self.is_active = True
        self.save()
