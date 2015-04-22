# -*- coding: utf-8 -*-
from django import forms

from django.contrib import admin
from django.contrib.admin import helpers
from django.contrib.admin.util import get_deleted_objects
from django.core.mail import mail_admins
from django.core.exceptions import PermissionDenied
from django.core.urlresolvers import reverse
from django.db import router
from django.template.response import TemplateResponse
from django.utils.encoding import force_text
from django.utils.translation import ugettext_lazy, ugettext as _

import autocomplete_light

from archives.models import Archive, Media, Participant, ArchiveParticipant
from events.models import ProgramNote
from utils.models import Role, Collectivity, Person, Work, Place, Composer

"""
Custom Model Admin
with factored merge feature
"""

class CustomModelAdmin(admin.ModelAdmin):

    actions = ['merge']

    def save_model(self, request, obj, form, change):
        if change:
            state = 'created'
        else:
            state = 'updated'
        obj.save()
        url = reverse('admin:%s_%s_change' % (obj._meta.app_label, obj._meta.module_name), args=[obj.id])
        mail_admins(u'[Archiprod] %s %s' % (obj.__unicode__(), state), u'<a href="%s">Edit %s</a>' % (url,  obj.__unicode__()))

    def merge_detail(self, queryset):
        raise NotImplementedError

    def merge(self, request, queryset):
        opts = self.model._meta
        app_label = opts.app_label
        # Check that the user has delete permission for the actual model
        if not self.has_delete_permission(request):
            raise PermissionDenied

        using = router.db_for_write(self.model)

        # Populate deletable_objects, a data structure of all related objects that
        # will also be deleted.
        deletable_objects, perms_needed, protected = get_deleted_objects(
            queryset, opts, request.user, self.admin_site, using)

        # The user has already confirmed the deletion.
        # Do the deletion and return a None to display the change list view again.
        if request.POST.get('post'):
            if perms_needed:
                raise PermissionDenied
            n = queryset.count()
            if n:
                self.merge_detail(queryset)
                message_bit = "%s items were" % n
                self.message_user(request, "%s successfully merged." % message_bit)
            # Return None to display the change list page again.
            return None

        if len(queryset) == 1:
            objects_name = force_text(opts.verbose_name)
        else:
            objects_name = force_text(opts.verbose_name_plural)

        #print objects_name

        if perms_needed or protected:
            title = _("Cannot merge %(name)s") % {"name": objects_name}
        else:
            title = _("Are you sure?")

        context = {
            "title": title,
            "objects_name": objects_name,
            "deletable_objects": [deletable_objects],
            'queryset': queryset,
            "perms_lacking": perms_needed,
            "protected": protected,
            "opts": opts,
            "app_label": app_label,
            'action_checkbox_name': helpers.ACTION_CHECKBOX_NAME,
        }

        # Display the confirmation page
        return TemplateResponse(request, self.delete_selected_confirmation_template or [
            "admin/%s/generic_confirm_merge.html" % app_label,
            "admin/generic_confirm_merge.html"
        ], context, current_app=self.admin_site.name)

    merge.short_description = ugettext_lazy("Merge selected %(verbose_name_plural)s")


"""
Role, Person, Collectivity, Work (with Composer) and Place Admin
"""

class RoleAdmin(CustomModelAdmin):
    list_display = ('label',)
    search_fields = ['label']

    def merge_detail(self, queryset):
        models = [Composer, ArchiveParticipant, Participant]
        for model in models:
            for role in queryset[1:]:
                items = model.objects.filter(role=role)
                for item in items:
                    item.role = queryset[0]
                    item.save()
        for role in queryset[1:]:
            role.delete()

    def change_view(self, request, object_id, extra_context=None):
        extra_context = extra_context or {}
        extra_context['archives'] = Archive.objects.filter(archiveparticipant__role__id=object_id)
        extra_context['medias'] = Media.objects.filter(participant__role__id=object_id)
        extra_context['programnotes'] = ProgramNote.objects.filter(noteparticipant__id=object_id)
        return super(RoleAdmin, self).change_view(request, object_id, extra_context=extra_context)


class PersonAdmin(CustomModelAdmin):
    list_display = ('id', 'last_name', 'first_name')
    search_fields = ['first_name', 'last_name']

    def merge_detail(self, queryset):
        models = [Composer, ArchiveParticipant, Participant]
        for model in models:
            for person in queryset[1:]:
                items = model.objects.filter(person=person)
                for item in items:
                    item.person = queryset[0]
                    item.save()
        for person in queryset[1:]:
            person.delete()

    def change_view(self, request, object_id, extra_context=None):
        extra_context = extra_context or {}
        extra_context['archives'] = Archive.objects.filter(archiveparticipant__person__id=object_id)
        extra_context['medias'] = Media.objects.filter(participant__person__id=object_id)
        extra_context['programnotes'] = ProgramNote.objects.filter(noteparticipant__person__id=object_id)
        extra_context['works'] = Work.objects.filter(composer__person__id=object_id)
        return super(PersonAdmin, self).change_view(request, object_id, extra_context=extra_context)


class CollectivityAdmin(CustomModelAdmin):
    list_display = ('name',)
    search_fields = ['name']

    def merge_detail(self, queryset):
        for collectivity in queryset[1:]:
            ws = Work.objects.filter(collectivities=collectivity)
            archives = Archive.objects.filter(collectivities=collectivity)
            medias = Media.objects.filter(collectivities=collectivity)
            for w in ws:
                w.collectivities.remove(collectivity)
                w.collectivities.add(queryset[0])
            for archive in archives:
                archive.collectivities.remove(collectivity)
                archive.collectivities.add(queryset[0])
            for media in medias:
                media.collectivities.remove(collectivity)
                media.collectivities.add(queryset[0])
        for collectivity in queryset[1:]:
            collectivity.delete()

    def change_view(self, request, object_id, extra_context=None):
        extra_context = extra_context or {}
        extra_context['archives'] = Archive.objects.filter(collectivities__id=object_id)
        extra_context['medias'] = Media.objects.filter(collectivities__id=object_id)
        return super(CollectivityAdmin, self).change_view(request, object_id, extra_context=extra_context)


class ComposerForm(forms.ModelForm):
    
    class Meta:
        model = Composer
        widgets = autocomplete_light.get_widgets_dict(Composer)


class ComposerInline(admin.TabularInline):
    model = Work.composers.through
    form = ComposerForm
    extra = 1


def composers_list(obj):
    return ", ".join(["%s %s" % (composer.last_name, composer.first_name) for composer in obj.composers.all()])


class WorkAdmin(CustomModelAdmin):
    list_display = ('id', 'title', 'subtitle', 'year', composers_list,)
    search_fields = ['title', 'subtitle']
    
    model = Work
    form = autocomplete_light.modelform_factory(Work)
    
    inlines = [ComposerInline, ]

    def merge_detail(self, queryset):
        Media.objects.filter(work__in=queryset).update(work=queryset[0])
        for work in queryset[1:]:
            work.delete()

    def change_view(self, request, object_id, extra_context=None):
        extra_context = extra_context or {}
        extra_context['medias'] = Media.objects.filter(work__id=object_id)
        return super(WorkAdmin, self).change_view(request, object_id, extra_context=extra_context)


class PlaceAdmin(CustomModelAdmin):
    list_display = ('name', 'hall', 'country', 'city')
    list_filter = ('country',)
    search_fields = ['name', 'hall']

    def merge_detail(self, queryset):
        Archive.objects.filter(place__in=queryset).update(place=queryset[0])
        for place in queryset[1:]:
            place.delete()

    def change_view(self, request, object_id, extra_context=None):
        extra_context = extra_context or {}
        extra_context['archives'] = Archive.objects.filter(place__id=object_id)
        return super(PlaceAdmin, self).change_view(request, object_id, extra_context=extra_context)


admin.site.register(Person, PersonAdmin)
admin.site.register(Role, RoleAdmin)
admin.site.register(Collectivity, CollectivityAdmin)
admin.site.register(Work, WorkAdmin)
admin.site.register(Place, PlaceAdmin)
