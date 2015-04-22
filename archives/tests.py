# -*- coding: utf-8 -*-
from datetime import datetime
from datetime import date
import os
import shutil
import re
import subprocess
from os.path import dirname, abspath

from django.conf import settings
from django.contrib.admin.sites import AdminSite
from django.core.management import call_command
from django.core.management.base import CommandError
from django.core.urlresolvers import reverse
from django.test import TestCase, Client
from django.test.client import RequestFactory
from django.test.utils import override_settings
from django.utils.encoding import force_str, force_text
from django.core.files import File

import django_rq
from django_rq import get_worker
from rq import get_current_job, Queue
import haystack
from django_rq.queues import (
    get_connection, get_queue, get_queue_by_index, get_queues,
    get_unique_connection_configs
)

from archives import archives_settings
from archives.factories import UserFactory, MediaFactory, ArchiveFactory, EventFactory, SetFactory
from archives.models import get_media_duration, VIDEO_EXTENSIONS, AUDIO_EXTENSIONS, Media, Set, ENCODING_NO_FILE, ENCODING_ENCODED, ENCODING_NOT_ENCODED, ENCODING_IN_QUEUE, ENCODING_IN_PROGRESS, ENCODING_FAILED
from utils.factories import WorkFactory


TEST_INDEX = {
    'default': {
    'ENGINE': 'haystack.backends.solr_backend.SolrEngine',
    'URL': 'http://127.0.0.1:8983/solr/test'
    },
}

TEST_STREAM= os.path.join(abspath(dirname(__file__)), 'tests/stream')
TEST_FTP = os.path.join(abspath(dirname(__file__)), 'tests/ftp')
TEST_MEDIA = os.path.join(abspath(dirname(__file__)), 'tests/media')

def access_self():
    job = get_current_job()
    return job.id


@override_settings(HAYSTACK_CONNECTIONS=TEST_INDEX, RQ_QUEUES=settings.RQ_QUEUES, STREAM_ROOT=TEST_STREAM, FTP_ROOT=TEST_FTP, MEDIA_ROOT=TEST_MEDIA)
class BaseTestCase(TestCase):
    """
    BaseTestCase setUp and tearDown:
    - the solr test instance
    - the rq
    """
    def setUp(self):
        for queueConfig in settings.RQ_QUEUES.itervalues():
            queueConfig['ASYNC'] = False

        haystack.connections.reload('default')
        # init django_rq
        q = django_rq.get_failed_queue()
        q.empty()
        q_archive = django_rq.get_queue('default')
        q_archive.empty()
        q_default = django_rq.get_queue('archive')
        q_default.empty()
        # must redefine archives_settings constant because archives_settings overriding not possible
        archives_settings.STREAM_EXT_AUDIO_ROOT = os.path.join(settings.STREAM_ROOT, 'ext', 'audio')
        archives_settings.STREAM_EXT_VIDEO_ROOT = os.path.join(settings.STREAM_ROOT, 'ext', 'video')
        archives_settings.STREAM_INT_AUDIO_ROOT = os.path.join(settings.STREAM_ROOT, 'int', 'audio')
        archives_settings.STREAM_INT_VIDEO_ROOT = os.path.join(settings.STREAM_ROOT, 'int', 'video')

        super(BaseTestCase, self).setUp()

    def tearDown(self):
        call_command('clear_index', interactive=False, verbosity=0)


class BaseAsyncTestCase(BaseTestCase):
    """
    BaseAsyncTestCase setUp :
    - ASYNC = True
    """
    def setUp(self):
        for queueConfig in settings.RQ_QUEUES.itervalues():
            queueConfig['ASYNC'] = True

        haystack.connections.reload('default')
        # init django_rq
        q = django_rq.get_failed_queue()
        q.empty()
        q_archive = django_rq.get_queue('archive')
        q_archive.empty()
        q_default = django_rq.get_queue('default')
        q_default.empty()
        # must redefine archives_settings constant because archives_settings overriding not possible
        archives_settings.STREAM_EXT_AUDIO_ROOT = os.path.join(settings.STREAM_ROOT, 'ext', 'audio')
        archives_settings.STREAM_EXT_VIDEO_ROOT = os.path.join(settings.STREAM_ROOT, 'ext', 'video')
        archives_settings.STREAM_INT_AUDIO_ROOT = os.path.join(settings.STREAM_ROOT, 'int', 'audio')
        archives_settings.STREAM_INT_VIDEO_ROOT = os.path.join(settings.STREAM_ROOT, 'int', 'video')

        super(BaseTestCase, self).setUp()


def create_without_encoding(media):
    # Helper to create instances of media, without async encoding to speed up tests
    # We create here empty files in stream directories for audio or video media files

    media.save(encode=False)

    if media.mime_type.startswith('video'):
        base_file_path_encoded_ext = os.path.join(archives_settings.STREAM_EXT_VIDEO_ROOT, str(media.file))
        base_file_path_encoded_int = os.path.join(archives_settings.STREAM_INT_VIDEO_ROOT, str(media.file))
        extensions = VIDEO_EXTENSIONS
    else:
        base_file_path_encoded_ext = os.path.join(archives_settings.STREAM_EXT_AUDIO_ROOT, str(media.file))
        base_file_path_encoded_int = os.path.join(archives_settings.STREAM_INT_AUDIO_ROOT, str(media.file))
        extensions = AUDIO_EXTENSIONS

    dir_file_encoded_ext = os.path.dirname(base_file_path_encoded_ext)
    dir_file_encoded_int = os.path.dirname(base_file_path_encoded_int)

    if not os.path.exists(dir_file_encoded_ext):
        os.makedirs(dir_file_encoded_ext)
    if not os.path.exists(dir_file_encoded_int):
        os.makedirs(dir_file_encoded_int)

    for extension in extensions:
        open("%s.%s" % (base_file_path_encoded_ext, extension), 'a').close()
        open("%s.%s" % (base_file_path_encoded_int, extension), 'a').close()


class HomeTests(BaseTestCase):
    """
    Home Tests
    """
    def setUp(self):
        print settings.DATABASES

        super(HomeTests, self).setUp()
        self.client = Client()

    def test_reach_homepage_no_sets(self):
        response = self.client.get(reverse('home'))
        self.assertEqual(response.status_code, 404)

    def test_reach_homepage_with_medias(self):
        # Build sets / archives / medias
        for bloc in settings.HOME_SETTINGS:
            if bloc['sets'] is not None:
                for set_id in bloc['sets']:
                    try:
                        self.set = SetFactory(id=set_id)
                    except:
                        self.set = Set.objects.get(id=set_id)
                    self.archive = ArchiveFactory(set=self.set)
                    self.media = MediaFactory.build(confidentiality='0', archive=self.archive)
                    create_without_encoding(self.media)
        # Create a media related to a work
        self.work = WorkFactory()
        self.media = MediaFactory.build(confidentiality='0', work=self.work)
        create_without_encoding(self.media)
        response = self.client.get(reverse('home'))
        self.assertEqual(response.status_code, 200)


class DetailBaseTests(BaseTestCase):
    """
    Detail Base Tests used to build needed media
    to test if they are reachable (see child classes)
    """
    def setUp(self):
        super(DetailBaseTests, self).setUp()
        self.media0 = MediaFactory.build(confidentiality='0') # internet
        self.media1 = MediaFactory.build(confidentiality='1') # intranet
        self.media2 = MediaFactory.build(confidentiality='2') # interdit

        self.archive0 = ArchiveFactory()
        self.media0_archive0 = MediaFactory.build(confidentiality='0', archive=self.archive0) # internet
        self.media1_archive0 = MediaFactory.build(confidentiality='0', archive=self.archive0) # internet

        self.archive1 = ArchiveFactory()
        self.media0_archive1 = MediaFactory.build(confidentiality='0', archive=self.archive1) # internet

        create_without_encoding(self.media0)
        create_without_encoding(self.media1)
        create_without_encoding(self.media2)
        create_without_encoding(self.media0_archive0)
        create_without_encoding(self.media1_archive0)
        create_without_encoding(self.media0_archive1)


class DetailTests(DetailBaseTests):
    """
    Detail Tests
    """
    def setUp(self):
        super(DetailTests, self).setUp()
        self.client = Client()

    def test_reach_media_no_archive(self):
        response = self.client.get(reverse('detail', args=[self.media0.id, ]))
        self.assertEqual(response.status_code, 200)
        self.assertTrue(response.context['other_archive_medias'] == None)

    def test_reach_media_linked_to_other_via_archive(self):
        response = self.client.get(reverse('detail', args=[self.media1_archive0.id, ]))
        self.assertEqual(response.status_code, 200)
        self.assertFalse(response.context['other_archive_medias'] == None)

    def test_reach_media_not_linked_to_other_via_archive(self):
        response = self.client.get(reverse('detail', args=[self.media0_archive1.id, ]))
        self.assertEqual(response.status_code, 200)
        self.assertTrue(response.context['other_archive_medias'] == None)


class DetailIntranetTests(DetailBaseTests):
    """
    Detail Intranet Tests
    """
    def setUp(self):
        super(DetailIntranetTests, self).setUp()
        # Set client ip inside Ircam
        self.client = Client(REMOTE_ADDR='129.102.64.20')

    def test_reach_an_internet_available_media(self):
        response = self.client.get(reverse('detail', args=[self.media0.id, ]))
        self.assertEqual(response.status_code, 200)
        # Here we check that path to file is present in the response
        self.assertTrue(str(self.media0.file) in response.content)

    def test_reach_an_intranet_available_media(self):
        response = self.client.get(reverse('detail', args=[self.media1.id, ]))
        self.assertEqual(response.status_code, 200)
        # Here we check that path to file is present in the response
        self.assertTrue(str(self.media1.file) in response.content)

    def test_reach_a_forbidden_media(self):
        response = self.client.get(reverse('detail', args=[self.media2.id, ]))
        self.assertEqual(response.status_code, 404)


class DetailInternetTests(DetailBaseTests):
    """
    Detail Internet Tests
    """
    def setUp(self):
        super(DetailInternetTests, self).setUp()
        # Set client ip outside Ircam
        self.client = Client(REMOTE_ADDR='121.102.64.20')

    def test_reach_an_internet_available_media(self):
        response = self.client.get(reverse('detail', args=[self.media0.id, ]))
        self.assertEqual(response.status_code, 200)
        # Here we check that path to file is present in the response
        self.assertTrue(str(self.media0.file) in response.content)

    def test_reach_an_intranet_available_media(self):
        response = self.client.get(reverse('detail', args=[self.media1.id, ]))
        self.assertEqual(response.status_code, 200)
        # Here we check that path to file is not present in the response
        self.assertFalse(str(self.media1.file) in response.content)

    def test_reach_a_forbidden_media(self):
        response = self.client.get(reverse('detail', args=[self.media2.id, ]))
        self.assertEqual(response.status_code, 404)


class SearchTests(BaseTestCase):
    """
    Search Tests
    """
    def setUp(self):
        super(SearchTests, self).setUp()
        self.client = Client()
        self.event1 = EventFactory(title='2012-1013')
        self.event2 = EventFactory(title='1998-1999')
        self.event3 = EventFactory(title='1990-1991')
        self.set1 = SetFactory(label='TitleSet1', comment='test recherche avec filtre série1')
        self.set2 = SetFactory(label='TitleSet2', comment='test recherche avec filtre série2')
        self.set3 = SetFactory(label='TitleSet3', comment='test recherche avec filtre série3')
        self.archive1 = ArchiveFactory(title='TitleArchive1', set=self.set1, event=self.event1, date=date(1978, 1, 1))
        self.archive2 = ArchiveFactory(title='TitleArchive2', set=self.set2, event=self.event2, date=date(1988, 1, 1))
        self.archive3 = ArchiveFactory(title='TitleArchive3', set=self.set3, event=self.event3, date=date(1998, 1, 1))
        self.media1 = MediaFactory.build(title='TitleMedia1', archive=self.archive1)
        self.media2 = MediaFactory.build(title='TitleMedia2', archive=self.archive2)
        self.media3 = MediaFactory.build(title='TitleMedia3', archive=self.archive3)
        self.media4 = MediaFactory.build(title='TitleMedia4 TitleMedia1')
        self.media5 = MediaFactory.build(title='TitleMedia5', comments='TitleMedia1')
        self.media6 = MediaFactory.build(title='TitleMedia6', comments='éééèèèèèèêêêààààààà')
        create_without_encoding(self.media1)
        create_without_encoding(self.media2)
        create_without_encoding(self.media3)
        create_without_encoding(self.media4)
        create_without_encoding(self.media5)
        create_without_encoding(self.media6)

    def test_reach_search(self):
        response = self.client.get(reverse('haystack_search'))
        self.assertEqual(response.status_code, 200)
        # check that without search params, we have all results diplayed
        self.assertEqual(len(response.context['page'].object_list), 6)

    def test_reach_search_simple_query(self):
        response = self.client.get(reverse('haystack_search'), data={'q':'TitleMedia1'})
        self.assertEqual(response.status_code, 200)
        # check that the number of results is fine
        self.assertEqual(len(response.context['page'].object_list), 3)

    def test_reach_search_empty_query(self):
        response = self.client.get(reverse('haystack_search'), data={'q':''})
        self.assertEqual(response.status_code, 200)
        # check that the number of results is fine
        self.assertEqual(len(response.context['page'].object_list), 6)

    def test_reach_search_no_results(self):
        response = self.client.get(reverse('haystack_search'), data={'q':'blabla'})
        self.assertEqual(response.status_code, 200)
        self.assertEqual(len(response.context['page'].object_list), 0)

    def test_reach_search_with_accents(self):
        response = self.client.get(reverse('haystack_search'), data={'q':'éééèèèèèèêêêààààààà'})
        self.assertEqual(response.status_code, 200)
        self.assertEqual(len(response.context['page'].object_list), 1)

    def test_reach_search_set_filter(self):
        response = self.client.get(reverse('haystack_search'), data={'q':'TitleMedia1', 'selected_facets':'set_exact:TitleSet1'})
        self.assertEqual(response.status_code, 200)
        self.assertEqual(len(response.context['page'].object_list), 1)

    def test_reach_search_year_filter(self):
        response = self.client.get(reverse('haystack_search'), data={'years':self.archive1.date.year})
        self.assertEqual(response.status_code, 200)
        self.assertEqual(len(response.context['page'].object_list), Media.objects.filter(archive__date__year=self.archive1.date.year).count())


class MediaAdminTest(BaseTestCase):
    """
    MediaAdminTest
    """
    def setUp(self):
        super(MediaAdminTest, self).setUp()
        self.site = AdminSite()
        self.factory = RequestFactory()
        self.user = UserFactory()

    def test_create_media(self):
        # We must import MediaAdmin here and not in the header
        # otherwise it's loaded before settings and thus, fails.
        from .admin import MediaAdmin
        ma = MediaAdmin(Media, self.site)
        request = self.factory.get('/admin/archives/media/add')
        request.user = self.user
        obj =  MediaFactory.build()
        # As obj is not saved, it hasn't got an id
        self.assertEqual(obj.id, None)
        ma.save_model(request, obj, None, False)
        # Below, we ensure that object has been created as it has an id.
        self.assertTrue(isinstance(obj.id, int))
        get_worker().work(burst=True)
        # add media with file
        # test if it's encoded
        # and test if
        # ! be carefull, this must be done using the admin save_model
        # and not the media save (for the moment may be)

    def test_update_media(self):
        pass

    def test_encode_action(self):
        # test if the encode action do the job
        # this is no the place to test encode management command
        pass

    def test_archive_action(self):
        # test if the archive action do the job
        # this is not the place to test archive management command
        pass


class MediaAsyncStateTest(BaseAsyncTestCase):
    """
    MediaAsyncStateTest 
    with ASYNC=True
    test in progress, in queue, failed states
    """
    def setUp(self):
        super(MediaAsyncStateTest, self).setUp()
    
    def test_async(self):
        # Make sure asynchronous is True
        queue = get_queue('default')
        self.assertTrue(queue._async)

    def test_get_worker_default(self):
        """
        By default, ``get_worker`` should return worker for ``default`` queue.
        """
        worker = get_worker()
        queue = worker.queues[0]
        self.assertEqual(queue.name, 'default')

    def test_get_current_job(self):
        """
        Ensure that functions using RQ's ``get_current_job`` doesn't fail
        when run from rqworker (the job id is not in the failed queue).
        """
        queue = get_queue()
        job = queue.enqueue(access_self)
        call_command('rqworker', burst=True)
        failed_queue = Queue(name='failed', connection=queue.connection)
        self.assertFalse(job.id in failed_queue.job_ids)
        job.delete()

    def test_media_encoded_state(self):
        #we create media without encoding
        self.media = MediaFactory.build(title='test_media_encoded_state', file__from_path=os.path.join(os.path.dirname(__file__), 'tests/data/audio-mini.mp3'))
        self.media.save(encode=False)
        
        #check it has been well created and encoding state is not encoded
        self.assertEqual(self.media.id, 1)
        self.assertEqual(self.media.encoding_state, ENCODING_NOT_ENCODED)

        #put it in encoding queue
        queue = django_rq.get_queue('default')
        job = queue.enqueue(call_command, args=('encode', self.media.id))

        #check job is in encoding queue
        self.assertTrue(job.is_queued)

        #start encoding
        worker = get_worker('default')
        worker.work(burst=True)

        #check encoding state is encoded, job is now in finished status
        self.assertEqual(self.media.encoding_state, ENCODING_ENCODED)
        self.assertFalse(job.is_queued)
        self.assertTrue(job.is_finished)
        failed_queue = Queue(name='failed', connection=queue.connection)
        self.assertFalse(job.id in failed_queue.job_ids)

    def test_media_inqueue_state(self):
        #we create media without encoding
        self.media = MediaFactory.build(title='test_media_inqueue_state', file__from_path=os.path.join(os.path.dirname(__file__), 'tests/data/audio-mini.mp3'))
        self.media.save(encode=False)
        
        #check it has been well created and encoding state is not encoded
        self.assertEqual(self.media.id, 1)
        self.assertEqual(self.media.encoding_state, ENCODING_NOT_ENCODED)

        #put it in encoding queue
        queue = django_rq.get_queue('default')
        job = queue.enqueue(call_command, args=('encode', self.media.id))

        #we don't start encoding
        #check encoding state is not encoded, job is still in inqueue status
        self.assertEqual(self.media.encoding_state, ENCODING_NOT_ENCODED)
        self.assertTrue(job.is_queued)
        self.assertFalse(job.is_finished)
        failed_queue = Queue(name='failed', connection=queue.connection)
        self.assertFalse(job.id in failed_queue.job_ids)

    def test_media_failed_state(self):
        #we create a wrong media without encoding
        self.media = MediaFactory.build(title='test_media_failed_state', file__from_path=os.path.join(os.path.dirname(__file__), 'tests/data/testwrongfile.txt'))
        self.media.save(encode=False)

        #put it in encoding queue
        queue = django_rq.get_queue('default')
        job = queue.enqueue(call_command, args=('encode', self.media.id))

        #check job is in encoding queue
        self.assertTrue(job.is_queued)

        #start encoding
        worker = get_worker('default')
        worker.work(burst=True)

        #check encoding state is not encoded, job is in failed queue
        self.assertEqual(self.media.encoding_state, ENCODING_NOT_ENCODED)
        self.assertFalse(job.is_queued)
        self.assertFalse(job.is_finished)
        failed_queue = Queue(name='failed', connection=queue.connection)
        self.assertTrue(job.id in failed_queue.job_ids)

    def test_media_inprogress_state(self):
        '''
        #we create media without encoding
        self.media = MediaFactory.build(title='test_media_inprogress_state', file__from_path=os.path.join(os.path.dirname(__file__), 'tests/data/audio-mini.mp3'))
        self.media.save(encode=False)

        #check it has been well created and encoding state is not encoded
        self.assertEqual(self.media.id, 1)
        self.assertEqual(self.media.encoding_state, ENCODING_NOT_ENCODED)

        #put it in encoding queue
        queue = django_rq.get_queue('default')
        job = queue.enqueue(call_command, args=('encode', self.media.id))

        #check job is in encoding queue
        self.assertTrue(job.is_queued)

        #start encoding
        worker = get_worker('default')
        worker.work(burst=True)

        #have to find a way to exit call_command (background process ?) and check job status
        #must be in started status then in finished status -> means in progress
        #self.assertTrue(job.is_started)
        '''
        pass

class MediaStateTest(BaseTestCase):
    """
    MediaStateTest
    """
    def setUp(self):
        super(MediaStateTest, self).setUp()

    def test_sync(self):
        # Make sure asynchronous is False
        queue = get_queue('default')
        self.assertFalse(queue._async)

    def test_media_encoded_state(self):
        self.media = MediaFactory(file__from_path=os.path.join(os.path.dirname(__file__), 'tests/data/audio-mini.mp3'))
        self.assertEqual(self.media.encoding_state, ENCODING_ENCODED)
 
    def test_media_notencoded_state(self):
        self.media = MediaFactory.build()
        self.assertEqual(self.media.encoding_state, ENCODING_NOT_ENCODED)

    def test_media_nofile_state(self):
        self.media = MediaFactory.build(file=None)
        self.assertEqual(self.media.encoding_state, ENCODING_NO_FILE)


class EncodeCommandTest(BaseTestCase):
    """
    EncodeCommandTest
    """
    def setUp(self):
        super(EncodeCommandTest, self).setUp()
        self.FMT = '%H:%M:%S.%f'

    def test_no_media(self):
        # we test a none video (id = 0) raises an error in encode call_command
        self.assertRaises(CommandError, call_command, 'encode', 0)

    def test_video_encode(self):
        # we test if video input is over 720p, video output is 720p y size
        self.video = MediaFactory(file__from_path=os.path.join(os.path.dirname(__file__), 'tests/data/video.mov'))
        for path in self.video.intranet_paths + self.video.internet_paths:
            process = subprocess.Popen(["ffmpeg", "-i", path], stdout=subprocess.PIPE, stderr=subprocess.STDOUT)
            stdout, stderr = process.communicate()
            pattern = re.compile(r', ([\w.-]+)x([\w.-]+)')
            match = pattern.search(stdout)
            y = match.group(2)
            self.assertEquals(int(y), 720)

    def test_video_less720p_encode(self):
        # we test that encoded file has more or less the same duration as input file
        # we test that a video in y size less than 720p is well encoded in original y size
        self.video = MediaFactory(file__from_path=os.path.join(os.path.dirname(__file__), 'tests/data/video_less720p.mov'))
        original_duration = datetime.strptime(self.video.duration, self.FMT)
        for path in self.video.intranet_paths + self.video.internet_paths:
            encoded_duration = datetime.strptime(get_media_duration(path), self.FMT)
            timedelta = abs(encoded_duration - original_duration).seconds
            self.assertTrue(timedelta < 10)

    def test_short_audio_encode_no_related_work(self):
        # we test that encoded file has more or less the same duration as input file
        self.audio_short = MediaFactory(file__from_path=os.path.join(os.path.dirname(__file__), 'tests/data/audio-short.mp3'))
        original_duration = datetime.strptime(self.audio_short.duration, self.FMT)
        for path in self.audio_short.intranet_paths + self.audio_short.internet_paths:
            encoded_duration = datetime.strptime(get_media_duration(path), self.FMT)
            timedelta = abs(encoded_duration - original_duration).seconds
            self.assertTrue(timedelta < 10)

    def test_long_audio_encode_no_related_work(self):
        # we test that encoded file has more or less the same duration as input file
        self.audio_long = MediaFactory(file__from_path=os.path.join(os.path.dirname(__file__), 'tests/data/audio-long.mp3'))
        original_duration = datetime.strptime(self.audio_long.duration, self.FMT)
        for path in self.audio_long.intranet_paths + self.audio_long.internet_paths:
            encoded_duration = datetime.strptime(get_media_duration(path), self.FMT)
            timedelta = abs(encoded_duration - original_duration).seconds
            self.assertTrue(timedelta < 10)

    def test_short_audio_encode_related_work(self):
        # we test that encoded file related to work, for a less than 12 mn media
        # is cut to 25% of its duration
        self.work = WorkFactory()
        self.audio_short_with_work = MediaFactory(file__from_path=os.path.join(os.path.dirname(__file__), 'tests/data/audio-short.mp3'), work=self.work)
        original_duration = datetime.strptime(self.audio_short_with_work.duration, self.FMT)
        target_internet_duration = datetime(1900, 1, 1, original_duration.hour/4, original_duration.minute/4, original_duration.second/4)
        for path in self.audio_short_with_work.internet_paths:
            encoded_duration = datetime.strptime(get_media_duration(path), self.FMT)
            timedelta = abs(encoded_duration - target_internet_duration).seconds
            self.assertTrue(timedelta < 10)
        for path in self.audio_short_with_work.intranet_paths:
            encoded_duration = datetime.strptime(get_media_duration(path), self.FMT)
            timedelta = abs(encoded_duration - original_duration).seconds
            self.assertTrue(timedelta < 10)

    def test_long_audio_encode_with_related_work(self):
        # we test that encoded file related to work, for a more than 12 mn media
        # is cut to 3mn duration
        self.work = WorkFactory()
        self.audio_long_with_work = MediaFactory(file__from_path=os.path.join(os.path.dirname(__file__), 'tests/data/audio-long.mp3'), work=self.work)
        original_duration = datetime.strptime(self.audio_long_with_work.duration, self.FMT)
        target_internet_duration = datetime(1900, 1, 1, 0, 3, 0)
        for path in self.audio_long_with_work.internet_paths:
            encoded_duration = datetime.strptime(get_media_duration(path), self.FMT)
            timedelta = abs(encoded_duration - target_internet_duration).seconds
            self.assertTrue(timedelta < 10)
        for path in self.audio_long_with_work.intranet_paths:
            encoded_duration = datetime.strptime(get_media_duration(path), self.FMT)
            timedelta = abs(encoded_duration - original_duration).seconds
            self.assertTrue(timedelta < 10)


class ArchiveCommandTest(BaseTestCase):
    """
    ArchiveCommandTest
    """
    def setUp(self):
        super(ArchiveCommandTest, self).setUp()

    def test_media_archive(self):
        # we copy video.mov from data test directory to TEST_FTP directory
        src = os.path.join(os.path.dirname(__file__), 'tests/data/audio-short.mp3')
        dst = os.path.join(TEST_FTP, 'audio-short.mp3')
        shutil.copyfile(src, dst)

        # we call command archive
        call_command('archive', 'audio-short.mp3')

        # we test if media has been well removed from TEST_FTP directory
        self.assertFalse(os.path.exists(dst))

        # we test if media has been well copied to MEDIA_ROOT
        destination_tmpl1 = os.path.join(settings.MEDIA_ROOT, 'files/%Y/%m/%d')
        destination_media = os.path.normpath(force_text(datetime.now().strftime(force_str(destination_tmpl1))))
        self.assertTrue(os.path.exists(os.path.join(destination_media, 'audio-short.mp3')))

        # we test if media encoded exists in STREAM_EXT_AUDIO_ROOT
        destination_tmpl2 = os.path.join(archives_settings.STREAM_EXT_AUDIO_ROOT, 'files/%Y/%m/%d')
        destination_stream = os.path.normpath(force_text(datetime.now().strftime(force_str(destination_tmpl2))))
        self.assertTrue(os.path.exists(os.path.join(destination_stream, 'audio-short.mp3.ogg')))
