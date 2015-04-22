# -*- coding: utf-8 -*-
from django.db import models
from mptt.models import MPTTModel, TreeForeignKey
from django.contrib.auth.models import User
from utils.models import Person, Role, Collectivity


class EventType(MPTTModel):
    """
    EventType
    """
    label = models.CharField(max_length=255)
    parent = TreeForeignKey('self', null=True, blank=True, related_name='children')

    def __unicode__(self):
        return self.label

    class MPTTMeta:
        order_insertion_by = ['label']


class Event(MPTTModel):
    """
    Event
    """
    title = models.CharField(max_length=255)
    subtitle = models.CharField(max_length=384, null=True, blank=True)
    parent = TreeForeignKey('self', null=True, blank=True, related_name='children', on_delete=models.SET_NULL)
    event_type = models.ForeignKey(EventType, null=True, blank=True)
    date_start = models.DateField(null=True, blank=True)
    date_end = models.DateField(null=True, blank=True)
    time_stamp = models.DateTimeField(auto_now=True)

    def _get_programs(self):
        """Return related event ProgramNotes that have associated file"""
        programs = []
        for event in self.get_ancestors(ascending=True, include_self=True):
            for program_note in event.programnote_set.all():
                if program_note.program:
                    programs.append(program_note)
        return programs
    programs = property(_get_programs)


    def __unicode__(self):
        return self.title

    class MPTTMeta:
        order_insertion_by = ['title']

    class Meta:
        # The TreeEditor needs this ordering definition
        ordering = ['tree_id', 'lft']


class ProgramNote(models.Model):
    """
    ProgramNote
    """
    CONFIDENTIALITE_CHOICES = (
        ('0', 'Non'),
        ('1', 'Oui / jamais utilisé dans archiprod actuel'),
    )
    ETAT_NOTE_CHOICES = (
        ('0', 'saisie incomplète'),
        ('1', 'saisie complète'),
    )
    id_loris = models.CharField(max_length=15, null=True, blank=True)
    title = models.CharField(max_length=255)
    comments = models.TextField(null=True, blank=True)
    nb_pages = models.IntegerField(null=True, blank=True)
    publisher = models.ForeignKey(Collectivity, null=True, blank=True)
    event = models.ForeignKey(Event)
    date_transfert = models.DateField(null=True, blank=True)
    user = models.ForeignKey(User, null=True, blank=True)
    confidentiality = models.CharField(max_length=1, choices=CONFIDENTIALITE_CHOICES)
    mime_type = models.CharField(max_length=765, null=True, blank=True)
    time_stamp = models.DateTimeField(auto_now=True)
    state = models.CharField(max_length=1, choices=ETAT_NOTE_CHOICES)
    program = models.FileField(upload_to="programs", null=True, blank=True)
    subtitle = models.CharField(max_length=384, null=True, blank=True)
    event_type = models.ForeignKey(EventType, null=True, blank=True)
    event = models.ForeignKey(Event, null=True, blank=True)
    participants = models.ManyToManyField(Person, null=True, blank=True, through='NoteParticipant')

    def _get_program_wm(self):
        return "%s-wm.pdf" % self.program.url[0:-4]
    program_wm = property(_get_program_wm)


    def __unicode__(self):
        return self.title


class NoteParticipant(models.Model):
    """
    NoteParticipant
    """
    program_note = models.ForeignKey(ProgramNote)
    person = models.ForeignKey(Person)
    role = models.ForeignKey(Role)
