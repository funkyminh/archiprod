# -*- coding: utf-8 -*-
from django import forms
from django.contrib import admin
from django.core.management import call_command
from django.core.mail import send_mail
from django.core.urlresolvers import reverse
from django.utils.translation import ugettext_lazy as _

from django.shortcuts import render_to_response
from django.conf.urls import patterns, url
from django.template import RequestContext


import django_rq
from rq.job import unpickle
import autocomplete_light

from archives.models import (ENCODING_ENCODED, ENCODING_STATES, Archive, Media,
                             Set, Tag, Contract, ArchiveParticipant, Participant, MediaCollectivity, ArchiveCollectivity,
                             Shared)
from utils.admin import CustomModelAdmin
from .forms import UploadFileFromServer


"""
Media admin
"""

class MediaParticipantForm(forms.ModelForm):

    class Meta:
        model = Participant
        widgets = autocomplete_light.get_widgets_dict(Participant)


class MediaParticipantInline(admin.TabularInline):
    model = Participant
    form = MediaParticipantForm
    extra = 1


class MediaCollectivityForm(forms.ModelForm):

    class Meta:
        model = MediaCollectivity
        widgets = autocomplete_light.get_widgets_dict(MediaCollectivity)


class MediaCollectivityInline(admin.TabularInline):
    model = MediaCollectivity
    form = MediaCollectivityForm
    extra = 1


class EncodingStateListFilter(admin.SimpleListFilter):
    """
    EncodingStateListFilter used to filter media by encoding state
    """
    title = _('encoding state')
    parameter_name = 'encoding_state'

    def lookups(self, request, model_admin):
        return ENCODING_STATES

    def queryset(self, request, queryset):
        # not optimum, but readable:
        # values below could have been computed
        # in specific if statements below
        # but it would have been cumbersome

        # UGLY hack to get current job
        # https://github.com/nvie/rq/pull/269
        in_progress_ids = []
        redis_conn = django_rq.get_connection()
        for k in redis_conn.keys():
            try:
                data = unpickle(redis_conn.hget(k, 'data'))
                status = redis_conn.hget(k, 'status')
                if data[0] == 'archives.admin.encode' and status == 'started':
                    in_progress_ids = [data[2][0], ]
                    break
            except:
                pass

        queue = django_rq.get_queue('default')
        in_queue_ids = [job.args[0] for job in queue.jobs
                        if job.func_name == 'archives.admin.encode']
        failed_queue = django_rq.get_failed_queue('default')
        failed_ids = [job.args[0] for job in failed_queue.jobs
                      if job.func_name == 'archives.admin.encode']

        if self.value() == 'no_file':
            # We can't do file__isnull for queryset
            # because FileField is represented internally
            # as a CharField, and Django stores non files
            # as an empty string '' in the database.
            return queryset.filter(file="")

        if self.value() == 'in_queue':
            return queryset.filter(id__in=in_queue_ids)

        if self.value() == 'in_progress':
            return queryset.filter(id__in=in_progress_ids)

        if self.value() == 'failed':
            return queryset.filter(id__in=failed_ids)

        if self.value() == 'encoded':
            encoded = [media.id for media in queryset if media.is_encoded]
            return queryset.exclude(file="").exclude(id__in=in_queue_ids)\
                           .exclude(id__in=in_progress_ids)\
                           .exclude(id__in=failed_ids).filter(id__in=encoded)

        if self.value() == 'not_encoded':
            not_encoded = [media.id for media in queryset if not media.is_encoded]
            return queryset.exclude(file="").exclude(id__in=in_progress_ids)\
                           .exclude(id__in=failed_ids).filter(id__in=not_encoded)\
                           .exclude(id__in=in_queue_ids)


class SameCommentsOrSummaryListFilter(admin.SimpleListFilter):

    title = _('same comments or summary as related archive')
    parameter_name = 'same_comments_or_summary'

    def lookups(self, request, model_admin):
        return (
            ('comments', _('same comments')),
            ('summary', _('same summary')),
        )

    def queryset(self, request, queryset):
        if self.value() == 'comments':
            q = queryset.select_related('archive').exclude(comments__isnull=True)
            r = [media.id for media in q if media.archive and media.comments == media.archive.comments]
            return q.filter(id__in = r)

        if self.value() == 'summary':
            q = queryset.select_related('archive').exclude(summary__isnull=True)
            r = [media.id for media in q if media.archive and media.summary == media.archive.summary]
            return q.filter(id__in = r)


class DailymotionListFilter(admin.SimpleListFilter):
    """
    DailymotionListFilter
    Used to filter media shared on Dailymotion
    """
    title = _('Available on Dailymotion')
    parameter_name = 'dailymotion'

    def lookups(self, request, model_admin):
        return (
            (1, 'Yes'),
            (0, 'No'),
        )

    def queryset(self, request, queryset):
        if self.value() is None:
            return queryset
        if int(self.value()) == 1:
            return queryset.filter(shared__dailymotion__isnull=False)
        if int(self.value()) == 0:
            return queryset.filter(shared__dailymotion__isnull=True)


class SoundcloudListFilter(admin.SimpleListFilter):
    """
    SoundcloudListFilter
    Used to filter media shared on Soundcloud
    """
    title = _('Available on Soundcloud')
    parameter_name = 'soundcloud'

    def lookups(self, request, model_admin):
        return (
            (1, 'Yes'),
            (0, 'No'),
        )

    def queryset(self, request, queryset):
        if self.value() is None:
            return queryset
        if int(self.value()) == 1:
            return queryset.filter(shared__soundcloud__isnull=False)
        if int(self.value()) == 0:
            return queryset.filter(shared__soundcloud__isnull=True)


class MediaTypeListFilter(admin.SimpleListFilter):
    """
    MediaTypeListFilter
    Used to filter media by type
    """
    title = _("Media type")
    parameter_name = 'media_type'

    def lookups(self, request, model_admin):
        return(
            ('audio', 'Audio'),
            ('video', 'Video'),
        )

    def queryset(self, request, queryset):
        if self.value() == 'audio':
            return queryset.filter(mime_type__istartswith='audio')
        if self.value() == 'video':
            return queryset.filter(mime_type__istartswith='video')

from django.forms import TextInput
from django.db import models

class MediaAdmin(admin.ModelAdmin):
    """
    Media admin
    """

    def formfield_for_dbfield(self, db_field, **kwargs):
        field = super(MediaAdmin, self).formfield_for_dbfield(db_field, **kwargs)
        if db_field.name == 'title':
            field.widget.attrs['style'] = 'width:80%;' + field.widget.attrs.get('style', '')
        return field

    #change_form_template = 'progressbarupload/change_form.html'
    #add_form_template = 'progressbarupload/change_form.html'
    list_display = ('id', 'title', 'work', 'archive_link', 'user', 'media',
                    'confidentiality', 'encoding_state_display', 'time_stamp',
                    'same_archive_comments', 'same_archive_summary', 'soundcloud', 'dailymotion')
    list_filter = ('user', EncodingStateListFilter, 'confidentiality', SameCommentsOrSummaryListFilter, DailymotionListFilter, SoundcloudListFilter, MediaTypeListFilter)
    raw_id_fields = ('archive',)
    search_fields = ['media', 'title', 'slug', 'work__title', 'archive__title']
    readonly_fields = ('mime_type', 'stream_files')
    save_on_top = True

    #def get_form(self, request, obj=None, **kwargs):
        #if request.user.is_superuser:
        #    kwargs['form'] = MySuperuserForm
        #return autocomplete_light.modelform_factory(Media)
        #super(MediaAdmin, self).get_form(request, obj, **kwargs)

    form = autocomplete_light.modelform_factory(Media)
    exclude = ('media',)

    inlines = [
        MediaParticipantInline, MediaCollectivityInline
    ]

    actions = ['launch_encodings', 'notify_providers']

    def archive_link(self, obj):
        if obj.archive:
            url = reverse('admin:%s_%s_change' % ('archives',  'archive'),  args=[obj.archive.id] )
            return '<a href="%s">%s</a>' % (url, obj.archive)
        return None
    archive_link.allow_tags = True
    archive_link.short_description = "archive"

    def queryset(self, request):
        qs = self.model.admin_objects.get_query_set()
        # TODO: this should be handled by some parameter to the ChangeList.
        # otherwise we might try to *None, which is bad ;)
        #ordering = self.ordering or ()
        #if ordering:
        #    qs = qs.order_by(*ordering)
        return qs

    def launch_encodings(self, request, queryset):
        # we exclude media without file, this
        # would directly go inside failed queue
        for media in queryset.exclude(file=''):
            # we shouldn't try to encode
            # media that are already in queue
            # or in progress

            # remove from failed queue
            failed_queue = django_rq.get_failed_queue()
            for job in failed_queue.jobs:
                if job.args[0] == media.id:
                    failed_queue.remove(job)
            queue = django_rq.get_queue('default')
            job = queue.enqueue(call_command, args=('encode', media.id, ), timeout=86400)

    launch_encodings.short_description = "Launch encoding jobs for selected medias"

    def notify_providers(self, request, queryset):
        for media in queryset:
            email = media.user.email
            url = reverse('detail', args=[media.slug])
            send_mail('[medias.ircam.fr] Uploaded media available', 'Here: http://medias.ircam.fr%s' % (url), 'medias@ircam.fr', [email], fail_silently=False)


    notify_providers.short_description = "Notify media provider that its media is available for selected media"

    def same_archive_comments(self, obj, *args):
        if obj.archive:
            if obj.archive.comments == obj.comments and obj.comments is not None:
                return True
        return False

    same_archive_comments.boolean = True

    def same_archive_summary(self, obj, *args):
        if obj.archive:
            if obj.archive.summary == obj.summary and obj.summary is not None:
                return True
        return False

    same_archive_summary.boolean = True

    def soundcloud(self, obj, *args):
        if obj.shared:
            if obj.shared.soundcloud:
                return True
        return False

    soundcloud.boolean = True

    def dailymotion(self, obj, *args):
        if obj.shared.dailymotion:
            return True
        return False

    dailymotion.boolean = True

    #def youtube(self, obj, *args):
    #    if obj.shared.youtube:
    #        return True
    #    return False

    #youtube.boolean = True

    #def vimeo(self, obj, *args):
    #    if obj.shared.vimeo:
    #        return True
    #    return False

    #vimeo.boolean = True

    def stream_files(self, instance):
        """ return links to stream files and player if file is encoded
        otherwise returns encoding state.
        """
        if instance.encoding_state == ENCODING_ENCODED:
            output = ''
            if instance.media_type == 'video':
                formats = ['mp4', 'ogg', 'webm']
            elif instance.media_type == 'audio':
                formats = ['mp3', 'ogg']
            else:
                return 'Error'
            for format in formats:
                output += "<a href='%(url)s.%(format)s' target='_blank'>%(url)s.%(format)s</a><br />" % {'url': instance.file_ext, 'format': format}
            if instance.media_type == 'video':
                output += '<video width="800" controls>'
                for format in formats:
                    output += '<source src="%(url)s.%(format)s" type="video/%(format)s">' % {'url': instance.file_ext, 'format': format}
                output += '</video>'
            if instance.media_type == 'audio':
                output += '<audio>'
                for format in formats:
                    output += '<source src="%(url)s.%(format)s" type="video/%(format)s">' % {'url': instance.file_ext, 'format': format}
                output += '</audio>'
            return output

        return self.get_encoding_state_display(instance)

    stream_files.allow_tags = True

    def save_model(self, request, obj, form, change):
        # Set user to the media
        if not change or obj.user is None:
            obj.user = request.user
        obj.save()

    # Upload from server utilities

    def _current_files_copied_in_queue(self):
        """ return current archives being processed (from server to archiprod) """
        _in_queue = []
        queue = django_rq.get_queue('archive')
        for index, job in enumerate(queue.jobs):
            _in_queue.append(job.args[0])
        return _in_queue

    def _current_file_copied_in_progress(self):
        """ return current files being copied """
        _in_progress = []
        redis_conn = django_rq.get_connection()
        for k in redis_conn.keys():
            try:
                data = unpickle(redis_conn.hget(k, 'data'))
                status = redis_conn.hget(k, 'status')
                if data[0] == 'archives.admin.archive' and status == 'started':
                    _in_progress = [data[2][0], ]
                    break
            except:
                pass
        return _in_progress

    def _failed_copies(self):
        """ return failed copies """
        failed_copies = []
        failed_queue = django_rq.get_failed_queue('archive')
        for index, job in enumerate(failed_queue.jobs):
            # HACK, BUG, FIXME : django-rq should return
            # only archive failed queue
            # but it returns old jobs failed !
            if job.func_name == 'archives.admin.archive':
                failed_copies.append(job.args[0])
        return failed_copies

    def old_fashioned_uploads(self, request):
        """ Admin view to upload file from archiprod-uploads server
        and monitor archive currently transfered.
        See archive command for effective archive transfert.
        """
        opts = self.model._meta
        app_label = opts.app_label
        if request.method == 'POST':
            form = UploadFileFromServer(request.POST)
            if form.is_valid():
                file_path = form.cleaned_data['file_path']
                media = form.cleaned_data['media']
                media_id = None
                if media is not None:
                    media_id = media.id
                queue = django_rq.get_queue('archive')
                queue.enqueue(call_command, args=('archive', file_path, media_id), timeout=86400)

        form = UploadFileFromServer()
        return render_to_response('admin/archives/media/upload-from-server.html',
                              {'form': form, 'app_label': app_label, 'opts':opts,
                               'current_files_copied_in_queue': self._current_files_copied_in_queue(),
                               'current_file_copied_in_progress': self._current_file_copied_in_progress(),
                               'failed_copies': self._failed_copies()
                               },
                              context_instance=RequestContext(request))


    def get_urls(self):
        urls = super(MediaAdmin, self).get_urls()
        my_urls = patterns('',
            url(r'^old-fashioned-uploads/$', self.admin_site.admin_view(self.old_fashioned_uploads), name="server-media-upload")
        )
        return my_urls + urls

"""
Archive admin
"""

class ArchiveParticipantForm(forms.ModelForm):
    class Meta:
        model = ArchiveParticipant
        widgets = autocomplete_light.get_widgets_dict(ArchiveParticipant)


class ArchiveParticipantInline(admin.TabularInline):
    model = Archive.participants.through
    form = ArchiveParticipantForm
    extra = 1


class ArchiveAdmin(admin.ModelAdmin):

    def formfield_for_dbfield(self, db_field, **kwargs):
        field = super(ArchiveAdmin, self).formfield_for_dbfield(db_field, **kwargs)
        if db_field.name in ['title', 'subtitle']:
            field.widget.attrs['style'] = 'width:80%;' + field.widget.attrs.get('style', '')
        return field

    list_display = ('id', 'id_archiprod', 'title', 'date', 'user', 'reviewer', 'event_link')
    list_filter = ('user',)
    date_hierarchy = 'date'
    search_fields = ['id_archiprod', 'title']

    form = autocomplete_light.modelform_factory(Archive)
    exclude = ['state', 'user', 'reviewer']
    raw_id_fields = ('event',)
    save_on_top = True
    readonly_fields = ('id_archiprod', 'available', 'pending')

    def event_link(self, obj):
        if obj.event:
            url = reverse('admin:%s_%s_change' % ('events',  'event'),  args=[obj.event.id] )
            return '<a href="%s">%s</a>' % (url, obj.event)
        return None
    event_link.allow_tags = True
    event_link.short_description = "event"

    def save_model(self, request, obj, form, change):
        if change:
            obj.reviewer = request.user
        else:
            obj.user = request.user
        obj.save()

    inlines = [
        ArchiveParticipantInline,
    ]

    def change_view(self, request, object_id, extra_context=None):
        extra_context = extra_context or {}
        extra_context['medias'] = Media.objects.filter(archive__id=object_id)
        return super(ArchiveAdmin, self).change_view(request, object_id, extra_context=extra_context)


"""
Set and Tag admin
"""

def years(obj):
    return ", ".join(list(obj.years))


def num_archives(obj):
    """ return number of archives for a set """
    return obj.archive_set.all().count()
num_archives.short_description = 'Number of related archives'


class SetAdmin(CustomModelAdmin):
    search_fields = ['label', ]
    list_display = ('id', 'label', num_archives, years,)
    actions = ['merge', 'unlink']

    def merge_detail(self, queryset):
        Archive.objects.filter(set__in=queryset).update(set=queryset[0])
        for set in queryset[1:]:
            set.delete()

    def unlink(self, request, queryset):
        Archive.objects.filter(set__in=queryset).update(set=None)

    def change_view(self, request, object_id, extra_context=None):
        extra_context = extra_context or {}
        extra_context['archives'] = Archive.objects.filter(set__id=object_id).order_by('-date', 'title' , 'event__title')
        return super(SetAdmin, self).change_view(request, object_id, extra_context=extra_context)

    unlink.short_description = _("Unlink %(verbose_name_plural)s from linked archives")


class TagAdmin(CustomModelAdmin):
    list_display = ('id', 'label', 'comment', 'nb_of_tagged_archives')
    search_fields = ['label', 'comment']

    def nb_of_tagged_archives(self, obj):
        return Archive.objects.filter(tags=obj).count()

    def merge_detail(self, queryset):
        archives = Archive.objects.filter(tags__in=queryset)
        for archive in archives:
            archive.tags.add(queryset[0])
        for tag in queryset[1:]:
            tag.delete()

    def change_view(self, request, object_id, extra_context=None):
        extra_context = extra_context or {}
        extra_context['archives'] = Archive.objects.filter(tags__id=object_id)
        return super(TagAdmin, self).change_view(request, object_id, extra_context=extra_context)


class SharedAdmin(admin.ModelAdmin):
    raw_id_fields = ("media",)


admin.site.register(Archive, ArchiveAdmin)
admin.site.register(Media, MediaAdmin)
admin.site.register(Tag, TagAdmin)
admin.site.register(Set, SetAdmin)
admin.site.register(Contract)
admin.site.register(Shared, SharedAdmin)
