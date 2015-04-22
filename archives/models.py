# -*- coding: utf-8 -*-
import mimetypes
import os
import re
import subprocess
import datetime
import base64

from binascii import hexlify

from django.contrib.auth.models import User
from django.core.urlresolvers import reverse
from django.conf import settings
from django.db import models
from django.utils.safestring import mark_safe
from django.template.defaultfilters import slugify
from django.utils.translation import ugettext_lazy as _
from django.core.management import call_command

import django_rq
from rq.job import unpickle

from utils.models import Person, Role, Collectivity, Place, Work
from events.models import Event

import archives_settings

if not settings.TESTING:
    # HACK: in case we test the app, we don't need to
    # import those models, which are only used in migration
    from acanthes import *


def get_media_duration(path):
    """
    Helper that returns media duration
    """
    process = subprocess.Popen(["ffmpeg", "-i", path], stdout=subprocess.PIPE, stderr=subprocess.STDOUT)
    stdout, stderr = process.communicate()
    try:
        pattern = re.compile(r'Duration: ([\w.-]+):([\w.-]+):([\w.-]+),')
        match = pattern.search(stdout)
        duration = "%s:%s:%s" % (match.group(1), match.group(2), match.group(3))
    except:
        duration = None
    return duration


class Tag(models.Model):
    """
    Tag
    """
    label = models.CharField(max_length=255)
    comment = models.TextField(null=True, blank=True)
    time_stamp = models.DateTimeField(auto_now=True)

    def __unicode__(self):
        return u"%s" % (self.label)


class Set(models.Model):
    """
    Set
    """
    label = models.CharField(max_length=255)
    comment = models.CharField(max_length=384, null=True, blank=True)
    time_stamp = models.DateTimeField(auto_now=True)

    def __unicode__(self):
        return u"%s" % (self.label)

    def _get_years(self):
        # FIXME try except is a ugly hack due to acanthes import pb.
        try:
            years = [e.get_ancestors()[0].title
                     for e in Event.objects.filter(archive__set=self)]
            return set(years)
        except:
            return set()
    years = property(_get_years)

    class Meta:
        ordering = ['label']


class Archive(models.Model):
    VOLTYPE_CHOICES = (
        ('1', '1 pour champs voltype ! a quoi cela sert'),
    )
    PRE_CHOICES = (
        ('0', '0'),  # 0 pour champs pret ! a quoi cela sert'
        ('1', '1'),  # 1 pour champs pret ! a quoi cela sert
    )
    ETAT_COLLECTION_CHOICES = (
        ('0', '0'),  # 0 pour champs etat collection ! a quoi cela sert
        ('1', '1'),  # 1 pour champs etat collection ! a quoi cela sert
    )
    PENDING_CHOICES = (
        ('0', '0'),  # 0 pour champs pending ! a quoi cela sert
        ('1', '1'),  # 1 pour champs pending ! a quoi cela sert
        ('2', '2'),  # 2 pour champs pending ! a quoi cela sert
    )

    id_archiprod = models.CharField(max_length=12)
    set = models.ForeignKey(Set, null=True, blank=True)
    tags = models.ManyToManyField(Tag, null=True, blank=True)
    event = models.ForeignKey(Event, null=True, blank=True)
    title = models.CharField(max_length=255, null=True, blank=True)
    subtitle = models.CharField(max_length=384, null=True, blank=True)
    date = models.DateField(null=True, blank=True)
    comments = models.TextField(null=True, blank=True)
    summary = models.TextField(null=True, blank=True)
    time_stamp = models.DateTimeField(auto_now=True)
    order = models.CharField(max_length=12, default=None, null=True, blank=True)
    user = models.ForeignKey(User, null=True, blank=True)
    reviewer = models.ForeignKey(User, null=True, blank=True, related_name='reviewer')
    place = models.ForeignKey(Place, null=True, blank=True)
    time = models.TimeField(null=True, blank=True)
    collectivities = models.ManyToManyField(Collectivity, null=True, blank=True, through='ArchiveCollectivity')
    #collectivities = models.ManyToManyField(Collectivity, null=True, blank=True)
    participants = models.ManyToManyField(Person, null=True, blank=True, through='ArchiveParticipant')
    old_id = models.CharField(max_length=384, null=True, blank=True)
    note2prog_id = models.CharField(max_length=30, null=True, blank=True)
    date_transfert = models.DateField(null=True, blank=True)
    available = models.CharField(max_length=1, choices=PRE_CHOICES, null=True, blank=True)  # pret
    state = models.CharField(max_length=1, choices=ETAT_COLLECTION_CHOICES, null=True, blank=True)  # etat_collection
    pending = models.CharField(max_length=1, choices=PENDING_CHOICES, null=True, blank=True)

    def __unicode__(self):
        if self.event and not self.title:
            return u"%s" % (self.event)
        return u"%s" % (self.title)


ENCODING_IN_QUEUE = 'in_queue'
ENCODING_IN_PROGRESS = 'in_progress'
ENCODING_FAILED = 'failed'
ENCODING_ENCODED = 'encoded'
ENCODING_NOT_ENCODED = 'not_encoded'
ENCODING_NO_FILE = 'no_file'

ENCODING_STATES = (
    (ENCODING_IN_QUEUE, _('In queue')),
    (ENCODING_IN_PROGRESS, _('In progress')),
    (ENCODING_FAILED, _('Failed')),
    (ENCODING_ENCODED, _('Encoded')),
    (ENCODING_NOT_ENCODED, _('Not encoded')),
    (ENCODING_NO_FILE, _('No file')),
)

ENCODING_STATES_DICT = dict(ENCODING_STATES)

AUDIO_EXTENSIONS = ['ogg', 'mp3']
VIDEO_EXTENSIONS = ['mp4', 'ogg', 'webm']


class MediaManager(models.Manager):
    def get_query_set(self):
        return super(MediaManager, self).get_query_set().exclude(confidentiality='2')


class Media(models.Model):

    CONFIDENTIALITE_PARTIE_CHOICES = (
        ('0', 'internet'),  # '0 pour champs etat confidentialite partie ! a quoi cela sert'
        ('1', 'intranet'),  # '1 pour champs etat confidentialite partie ! a quoi cela sert'
        ('2', 'interdit'),  # '2 pour champs etat confidentialite partie ! a quoi cela sert'
    )
    TYPE_RECORD_CHOICES = (
        ('0', 'Production'),
        ('1', 'Bonus'),
        ('2', 'Rush'),
    )

    media = models.CharField(max_length=36, null=True, blank=True)
    order = models.IntegerField(null=True, blank=True)
    archive = models.ForeignKey(Archive, null=True, blank=True)
    title = models.CharField(max_length=255, null=True, blank=True)
    duration = models.TimeField(null=True, blank=True)  # faire le nettoyage entre 00:00:00 et vide
    comments = models.TextField(null=True, blank=True)
    time_stamp = models.DateTimeField(auto_now=True)
    work = models.ForeignKey(Work, null=True, blank=True)
    publisher = models.ForeignKey(Collectivity, null=True, blank=True, related_name='publisher')
    confidentiality = models.CharField(max_length=1, choices=CONFIDENTIALITE_PARTIE_CHOICES, default='0')
    collectivities = models.ManyToManyField(Collectivity, null=True, blank=True, through='MediaCollectivity')   # collectivites
    #collectivities = models.ManyToManyField(Collectivity, null=True, blank=True)   # collectivites
    participants = models.ManyToManyField(Person, null=True, blank=True, through='Participant')
    file = models.FileField(max_length=1000, upload_to="files/%Y/%m/%d", null=True, blank=True)
    slideshow = models.FileField(upload_to="slideshows/%Y/%m/%d", null=True, blank=True)
    record_type = models.CharField(max_length=1, null=True, blank=True, choices=TYPE_RECORD_CHOICES)
    summary = models.TextField(null=True, blank=True)
    mime_type = models.CharField(max_length=192, null=True, blank=True)
    user = models.ForeignKey(User, null=True, blank=True)
    thumbnail = models.ImageField(upload_to='thumbnails', null=True, blank=True)
    slug = models.SlugField(unique=True, null=True, blank=True)

    objects = MediaManager()
    admin_objects = models.Manager()

    def _get_internet_basefilename_url(self):
        if self.file:
            if self.mime_type.startswith('video'):
                return os.path.join(archives_settings.STREAM_EXT_VIDEO_URL, str(self.file))
            else:
                return os.path.join(archives_settings.STREAM_EXT_AUDIO_URL, str(self.file))
        else:
            return ''

    def _get_intranet_basefilename_url(self):
        if self.file:
            if self.mime_type.startswith('video'):
                return os.path.join(archives_settings.STREAM_INT_VIDEO_URL, str(self.file))
            else:
                return os.path.join(archives_settings.STREAM_INT_AUDIO_URL, str(self.file))
        else:
            return ''

    def _get_intranet_urls(self):
        if self.encoding_state == ENCODING_ENCODED:
            if self.mime_type.startswith('video'):
                base_stream_path = archives_settings.STREAM_INT_VIDEO_URL
                extensions = VIDEO_EXTENSIONS
            else:
                base_stream_path = archives_settings.STREAM_INT_AUDIO_URL
                extensions = AUDIO_EXTENSIONS
            base_path = os.path.join(base_stream_path, str(self.file))
            return ["%s.%s" % (base_path, extension) for extension in extensions]
        else:
            return None

    def _get_internet_urls(self):
        if self.encoding_state == ENCODING_ENCODED:
            if self.mime_type.startswith('video'):
                base_stream_path = archives_settings.STREAM_EXT_VIDEO_URL
                extensions = VIDEO_EXTENSIONS
            else:
                base_stream_path = archives_settings.STREAM_EXT_AUDIO_URL
                extensions = AUDIO_EXTENSIONS
            base_path = os.path.join(base_stream_path, str(self.file))
            return ["%s.%s" % (base_path, extension) for extension in extensions]
        else:
            return None

    def _get_intranet_paths(self):
        if self.encoding_state == ENCODING_ENCODED:
            if self.mime_type.startswith('video'):
                base_stream_path = archives_settings.STREAM_INT_VIDEO_ROOT
                extensions = VIDEO_EXTENSIONS
            else:
                base_stream_path = archives_settings.STREAM_INT_AUDIO_ROOT
                extensions = AUDIO_EXTENSIONS
            base_path = os.path.join(base_stream_path, str(self.file))
            return ["%s.%s" % (base_path, extension) for extension in extensions]
        else:
            return None

    def _get_internet_paths(self):
        if self.encoding_state == ENCODING_ENCODED:
            if self.mime_type.startswith('video'):
                base_stream_path = archives_settings.STREAM_EXT_VIDEO_ROOT
                extensions = VIDEO_EXTENSIONS
            else:
                base_stream_path = archives_settings.STREAM_EXT_AUDIO_ROOT
                extensions = AUDIO_EXTENSIONS
            base_path = os.path.join(base_stream_path, str(self.file))
            return ["%s.%s" % (base_path, extension) for extension in extensions]
        else:
            return None

    def _is_sound(self):
        if self.work:
            return True
        return False

    def _media_type(self):
        try:
            if self.mime_type.startswith('video'):
                return 'video'
            return 'audio'
        except:
            return None

    def _event_type(self):
        try:
            return self.archive.event.event_type.id
        except:
            return None

    def _is_encoded(self):
        # Test if a file is encoded, should be used after
        # checking that file is not inside encoding queue
        # because, this test is based on existence of file
        # and during encoding pass, the file is created, so
        # we could have a file created, but not entirely encoded.
        audio_path = os.path.join(archives_settings.STREAM_EXT_AUDIO_ROOT, str(self.file)) + '.ogg'
        video_path = os.path.join(archives_settings.STREAM_EXT_VIDEO_ROOT, str(self.file)) + '.ogg'
        if any([os.path.exists(audio_path), os.path.exists(video_path)]):
            return True
        return False

    def _encoding_state(self):
        # No file associated with the media
        if not self.file:
            return ENCODING_NO_FILE

        # The file is currently processed
        redis_conn = django_rq.get_connection()
        for k in redis_conn.keys():
            try:
                data = unpickle(redis_conn.hget(k, 'data'))
                status = redis_conn.hget(k, 'status')
                if data[0] == 'archives.admin.encode' and status == 'started' and self.id == data[2][0]:
                    return ENCODING_IN_PROGRESS
            except:
                pass

        # The file is currently in queue for encoding process
        queue = django_rq.get_queue('default')
        for index, job in enumerate(queue.jobs):
            if job.func_name == 'archives.admin.encode':
                if job.args[0] == self.id:
                    return ENCODING_IN_QUEUE, index

        # If not, the encoding process should have failed
        failed_queue = django_rq.get_failed_queue('default')
        for job in failed_queue.jobs:
            if job.func_name == 'archives.admin.encode':
                if job.args[0] == self.id:
                    return ENCODING_FAILED

        # Or, there's no job for this media
        # So, we have two cases: the encoded files are available
        # and media is encoded, or files are not availabble
        # and we checked before that we weren't processing file
        # or having a 'failed' encoding process
        # so, the file is just 'not encoded'
        if self.file:
            # Test if files in stream repository exist
            if self.is_encoded:
                return ENCODING_ENCODED
            else:
                return ENCODING_NOT_ENCODED

    def _encoding_state_display(self):
        current_encoding_state = self.encoding_state
        if isinstance(current_encoding_state, tuple):
            # FIXME: waful python string formating % doesn't work
            # it returns me __proxy__
            state = ENCODING_STATES_DICT.get(self.encoding_state[0])
            return state + ' [' + str(current_encoding_state[1]) + ']'
        else:
            return ENCODING_STATES_DICT.get(current_encoding_state)

    def _get_size(self):
        """
        media size
        """
        process = subprocess.Popen(["ffmpeg", "-i", self.file.path], stdout=subprocess.PIPE, stderr=subprocess.STDOUT)
        stdout, stderr = process.communicate()
        size = []
        try:
            pattern = re.compile(r', ([\w.-]+)x([\w.-]+)')
            match = pattern.search(stdout)
            x = match.group(1)
            y = match.group(2)
            size.extend([x, y])
        except:
            size = None
        return size

    def _get_base64_links(self):
        if self.file:
            links = []
            now = datetime.datetime.now()
            url = self.file.url
            link = [url, base64.b64encode('%s||%s' % (url, now))]
            links.append(link)
            for l in self.internet_urls:
                url = l
                links.append([url, base64.b64encode('%s||%s' % (url, now))])
            for l in self.intranet_urls:
                url = l
                links.append([url, base64.b64encode('%s||%s' % (url, now))])
            return links
        return False

    base64_links = property(_get_base64_links)


    size = property(_get_size)
    file_ext = property(_get_internet_basefilename_url)
    file_int = property(_get_intranet_basefilename_url)
    intranet_urls = property(_get_intranet_urls)
    internet_urls = property(_get_internet_urls)
    intranet_paths = property(_get_intranet_paths)
    internet_paths = property(_get_internet_paths)

    is_sound = property(_is_sound)
    media_type = property(_media_type)
    event_type = property(_event_type)
    encoding_state = property(_encoding_state)
    encoding_state_display = property(_encoding_state_display)
    is_encoded = property(_is_encoded)

    def get_absolute_url(self):
        return reverse('detail', args=[self.slug, ])

    def __unicode__(self):
        if self.work:
            composers = ', '.join([c.__unicode__() for c in self.work.composers.all()])
            if self.title:
                if self.work.subtitle:
                    return mark_safe(u"<i>%s, %s</i> - %s, %s" % (self.work.title, self.work.subtitle, self.title, composers))
                else:
                    return mark_safe(u"<i>%s</i> - %s, %s" % (self.work.title, self.title, composers))
            return mark_safe(u"<i>%s</i>, %s" % (self.work.title, composers))
        else:
            return u"%s" % (self.title)

    def save(self, encode=True, *args, **kwargs):
        # Set slug to the media
        if not self.slug:
            if self.work:
                if self.work.composers :
                    composers = '-'.join(["%s" % (slugify(c.__unicode__())) for c in self.work.composers.all()])
                    self.slug = 'x%s_%s-%s' % (hexlify(os.urandom(3)), slugify(self.work.title), slugify(composers))
                else:
                    self.slug = 'x%s_%s' % (hexlify(os.urandom(3)), slugify(self.work.title))
                self.slug = self.slug[:50]
            elif self.title:
                self.slug = 'x%s_%s' % (hexlify(os.urandom(3)), slugify(self.title[:42]))
            else:
                self.slug = 'x%s' % hexlify(os.urandom(3))

        if self.file:
            # Set media duration (if file exists)

            self.duration = get_media_duration(self.file.path)
            # Set mimetype
            self.mime_type = mimetypes.guess_type(self.file.path)[0]
            if self.mime_type is None:
                # TODO: this is due to original archiprod archives files
                # guesstype doesn't find the mimetype because theses archives
                # doesn't have extension name
                if self.file.name.find('VI') != -1:
                    self.mime_type = 'video'

        super(Media, self).save(*args, **kwargs)
        # encode param allow to bypass the encoding process
        if self.file and encode:
            # Call asynchronous encode command
            if self.encoding_state == ENCODING_NOT_ENCODED:
                queue = django_rq.get_queue('default')
                queue.enqueue(call_command, args=('encode', self.id, ), timeout=86400)


class Contract(models.Model):
    """
    Contract
    """
    title = models.CharField(max_length=255)
    archive = models.ForeignKey(Archive)
    comments = models.TextField(null=True, blank=True)
    nb_pages = models.IntegerField(null=True, blank=True)
    user = models.ForeignKey(User)
    time_stamp = models.DateTimeField(auto_now=True)
    file = models.FileField(upload_to="contracts", null=True, blank=True)

    def __unicode__(self):
        return u"%s" % (self.title)


class ArchiveParticipant(models.Model):
    """
    ArchiveParticipant
    """
    archive = models.ForeignKey(Archive)
    person = models.ForeignKey(Person)
    #role = models.ForeignKey(Role)
    role = models.ManyToManyField(Role, null=True, blank=True, related_name="role_new1")

    def __unicode__(self):
        return u"%s %s" % (self.person.first_name, self.person.last_name)


class Participant(models.Model):
    """
    Participant
    """
    media = models.ForeignKey(Media)
    person = models.ForeignKey(Person)
    #role = models.ForeignKey(Role)
    role = models.ManyToManyField(Role, null=True, blank=True, related_name="role_new2")

    def __unicode__(self):
        return u"%s" % (self.person)


class ArchiveCollectivity(models.Model):
    """
    Archive Collectivity
    """
    archive = models.ForeignKey(Archive)
    collectivity = models.ForeignKey(Collectivity)
    #role = models.ForeignKey(Role, null=True, blank=True)
    role = models.ManyToManyField(Role, null=True, blank=True, related_name="role_new3")

    def __unicode__(self):
        return u"%s" % (self.collectivity.name)

    class Meta:
        db_table="archives_archive_collectivities"
        unique_together = (('archive', 'collectivity'))


class MediaCollectivity(models.Model):
    """
    Media Collectivity
    """
    media = models.ForeignKey(Media)
    collectivity = models.ForeignKey(Collectivity)
    #role = models.ForeignKey(Role, null=True, blank=True)
    role = models.ManyToManyField(Role, null=True, blank=True, related_name="role_new4")

    def __unicode__(self):
        return u"%s" % (self.collectivity.name)

    class Meta:
        db_table="archives_media_collectivities"
        unique_together = (('media', 'collectivity'))


class Shared(models.Model):
    """
    Shared, used to keep referenc of shared media on multiple web platforms
    """
    media = models.OneToOneField(Media)
    dailymotion = models.CharField(max_length=255, null=True, blank=True)
    vimeo = models.CharField(max_length=255, null=True, blank=True)
    youtube = models.CharField(max_length=255, null=True, blank=True)
    soundcloud = models.CharField(max_length=255, null=True, blank=True)

