# -*- coding: utf-8 -*-
from django.db import models


class Person(models.Model):
    """
    Person
    """

    first_name = models.CharField(max_length=150, blank=True, null=True)
    last_name = models.CharField(max_length=150)
    biography = models.TextField(blank=True, null=True)

    def __unicode__(self):
        return u"%s %s" % (self.first_name, self.last_name)

    class Meta:
        verbose_name_plural = "people"
        ordering = ['last_name']


class Role(models.Model):
    """
    Role
    """

    label = models.CharField(max_length=255)

    def __unicode__(self):
        return u"%s" % (self.label)


class Collectivity(models.Model):
    """
    Collectivity
    """

    name = models.CharField(max_length=255)
    description = models.TextField(blank=True, null=True)

    def __unicode__(self):
        return u"%s" % (self.name)

    class Meta:
        verbose_name_plural = "collectivities"
        ordering = ['name']


class Place(models.Model):
    """
    Place
    """

    name = models.CharField(max_length=255)
    hall = models.CharField(max_length=255, null=True, blank=True)
    country = models.CharField(max_length=765)
    city = models.CharField(max_length=765)

    def __unicode__(self):
        return u"%s %s %s %s" % (self.name, self.hall, self.country, self.city)


class Work(models.Model):
    """
    Work
    """

    title = models.CharField(max_length=384)
    subtitle = models.CharField(max_length=384, null=True, blank=True)
    year = models.CharField(max_length=12, null=True, blank=True)
    composers = models.ManyToManyField(Person, null=True, blank=True, through='Composer')
    collectivities = models.ManyToManyField(Collectivity, null=True, blank=True)

    def __unicode__(self):
        return u"%s %s" % (self.title, self.year)


class Composer(models.Model):
    """
    Composer
    """
    
    work = models.ForeignKey(Work)
    person = models.ForeignKey(Person)
    role = models.ForeignKey(Role)

    def __unicode__(self):
        return u"%s %s" % (self.person.first_name, self.person.last_name)
