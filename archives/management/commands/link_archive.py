# -*- coding: utf-8 -*-
import os

from django.conf import settings
from django.core.management.base import BaseCommand

from archives.models import Media
from events.models import ProgramNote


class Command(BaseCommand):
    help = '''From OLD_ARCHIVES_* directories, update file field of Media/ProgramNote models
              with related archive'''

    def handle(self, *args, **options):
        self.failed = 0
        self.successful = 0
        # Videos
        path_video = settings.OLD_ARCHIVES_VIDEO
        files_video = os.listdir(os.path.join(settings.MEDIA_ROOT, path_video))

        for file_video in files_video:
            self.link(file_video, os.path.join(path_video, file_video), 'video')

        # Audios
        path_audio = settings.OLD_ARCHIVES_AUDIO
        directories_audio = os.listdir(os.path.join(settings.MEDIA_ROOT, path_audio))

        for dir_audio in directories_audio:
            for file_audio in os.listdir(os.path.join(settings.MEDIA_ROOT, path_audio, dir_audio)):
                # HACK to fix '+1' in archive audiofile names in old archiprod
                file_audio_temp = file_audio[0:8] + '00' + str(int(file_audio[8:10])-1)
                self.link(file_audio_temp, os.path.join(path_audio, dir_audio, file_audio), 'audio')

        # Program notes
        path_programnote = settings.OLD_PROGRAM_NOTE
        files_programnote = os.listdir(os.path.join(settings.MEDIA_ROOT, path_programnote))

        for file_programnote in files_programnote:
            file_programnote_temp = file_programnote[2:7]
            try:
                programnote = ProgramNote.objects.get(id_loris=file_programnote_temp)
                ProgramNote.objects.filter(pk=programnote.id).update(program=path_programnote + file_programnote)
                self.successful += 1
            except ProgramNote.DoesNotExist, e:
                print e
                self.failed += 1

        print "Successful: %s, Failed: %s, Total: %s" % (self.successful,self.failed, self.successful + self.failed)

    def link(self, basename, path, mime_type):
        """ Set media.file to the right path for old archiprod medias """
        try:
            media = Media.objects.get(media=basename)
            media.file = path
            media.mime_type = mime_type
            media.save(encode=False)
            self.successful += 1
        except Media.DoesNotExist, e:
            print e
            self.failed += 1
