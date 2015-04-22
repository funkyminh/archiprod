# -*- coding: utf-8 -*-
import datetime
from django import forms
from django.contrib import admin
from django.core.management import call_command
from django.conf.urls import patterns, url
from django.shortcuts import render_to_response
from django.template import RequestContext

import autocomplete_light
from django_rq import job
from feincms.admin import tree_editor

from events.models import Event, EventType, ProgramNote, NoteParticipant
from archives.models import Archive


@job
def watermark(id):
    call_command('watermark', id)

"""
Event and EventType admin
"""

def num_events(obj):
    """ return number of events for an event_type """
    return obj.event_set.all().count()
num_events.short_description = 'Number of related events'


class EventTypeAdmin(tree_editor.TreeEditor):
    list_display = ('label', num_events)

    def change_view(self, request, object_id, extra_context=None):
        extra_context = extra_context or {}
        extra_context['events'] = Event.objects.filter(event_type__id=object_id)
        return super(EventTypeAdmin, self).change_view(request, object_id, extra_context=extra_context)


class ProgramNoteForm(forms.ModelForm):

    class Meta:
        model = ProgramNote
        widgets = autocomplete_light.get_widgets_dict(ProgramNote)


class ProgramNoteInline(admin.StackedInline):
    model = ProgramNote
    form = ProgramNoteForm
    readonly_fields = ('user',)
    exclude = ('subtitle',)
    extra = 1


class EventAdmin(tree_editor.TreeEditor):

    def formfield_for_dbfield(self, db_field, **kwargs):
        field = super(EventAdmin, self).formfield_for_dbfield(db_field, **kwargs)
        if db_field.name in ['title', 'subtitle']:
            field.widget.attrs['style'] = 'width:80%;' + field.widget.attrs.get('style', '')
        return field

    list_display = ('title', 'event_type', 'date_start', 'date_end')
    list_filter = ('event_type',)
    date_hierarchy = 'date_start'
    search_fields = ['title']
    save_on_top = True
    form = autocomplete_light.modelform_factory(Event)

    inlines = [ProgramNoteInline,]

    def change_view(self, request, object_id, extra_context=None):
        extra_context = extra_context or {}
        extra_context['archives'] = Archive.objects.filter(event__id=object_id)
        return super(EventAdmin, self).change_view(request, object_id, extra_context=extra_context)

    def save_formset(self, request, form, formset, change):
        """ Save program note formset and watermark pdf files """
        if formset.model != ProgramNote:
            return super(EventAdmin, self).save_formset(request, form, formset, change)
        instances = formset.save(commit=False)
        for instance in instances:
            instance.save()
            # Call watermark command for each program note instance saved.
            watermark(instance.pk)
        formset.save_m2m()

    def old_fashioned_tree(self, request, year):
        year = int(year)
        # get root events for year
        # filter(date_start__year=year).
        events = Event.objects.order_by('tree_id', 'lft')
        years = [i for i in range(1970, datetime.datetime.now().year+1)]
        opts = self.model._meta
        app_label = opts.app_label
        return render_to_response('admin/events/event/event-tree.html',
                              {'app_label': app_label, 'opts':opts, 'cl': {'opts':opts}, 'events': events, 'years':years, 'current_year': str(year)},
                              context_instance=RequestContext(request))

    def get_urls(self):
        urls = super(EventAdmin, self).get_urls()
        my_urls = patterns('',
            url(r'^old-fashioned-tree/(?P<year>\d*)$', self.admin_site.admin_view(self.old_fashioned_tree), name="event-tree")
        )
        return my_urls + urls


"""
ProgramNote admin
"""


class NoteParticipantForm(forms.ModelForm):

    class Meta:
        model = NoteParticipant
        widgets = autocomplete_light.get_widgets_dict(NoteParticipant)


class NoteParticipantInLine(admin.TabularInline):
    model = ProgramNote.participants.through
    form = NoteParticipantForm
    extra = 1


class ProgramNoteAdmin(admin.ModelAdmin):

    def formfield_for_dbfield(self, db_field, **kwargs):
        field = super(ProgramNoteAdmin, self).formfield_for_dbfield(db_field, **kwargs)
        if db_field.name in ['title', 'subtitle']:
            field.widget.attrs['style'] = 'width:80%;' + field.widget.attrs.get('style', '')
        return field

    list_display = ('title', 'id_loris')
    search_fields = ['title', 'id_loris',]

    form = autocomplete_light.modelform_factory(ProgramNote)
    raw_id_fields = ("event",)
    readonly_fields = ('user',)


    def save_model(self, request, obj, form, change):
        if not change:
            obj.user = request.user
        obj.save()
        watermark(obj.id)

    inlines = [
        NoteParticipantInLine,
    ]


admin.site.register(EventType, EventTypeAdmin)
admin.site.register(Event, EventAdmin)
admin.site.register(ProgramNote, ProgramNoteAdmin)
