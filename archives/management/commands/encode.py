# -*- coding: utf-8 -*-
import os
import mimetypes
import datetime
import sys

from converter import Converter, FFMpeg

from django.core.management.base import BaseCommand, CommandError
from django.conf import settings
from archives import archives_settings

from archives.models import Media

# Options for format containers and encodings

OPTIONS_MP4_pass1 = ['-pass', '1', '-pix_fmt', 'yuv420p', '-vcodec', 'libx264', '-preset', 'slow', '-b:v', '500k', '-maxrate', '500k', '-bufsize', '1000k', '-an', '-f', 'mp4']

OPTIONS_MP4_pass2 = ['-pass', '2', '-pix_fmt', 'yuv420p', '-vcodec', 'libx264', '-preset', 'slow', '-b:v', '500k', '-maxrate', '500k', '-bufsize', '1000k', '-codec:a', 'libfaac', '-b:a', '128k', '-f', 'mp4']

OPTIONS_WEBM = ['-codec:v', 'libvpx', '-quality', 'good', '-b:v', '1900K', '-crf', '8', '-codec:a', 'libvorbis', '-b:a', '192k', '-f', 'webm']

OPTIONS_OGV = ['-codec:v', 'libtheora', '-quality', 'good', '-q:v', '8', '-codec:a', 'libvorbis', '-q:a', '5', '-f', 'ogg']


OPTIONS_OGG = {
    'format': 'ogg',
    'audio': {'codec': 'vorbis'}
}

OPTIONS_MP3 = {
    'format': 'mp4',
    'audio': {'codec': 'mp3'}
}

# These 2 options below are a bit ugly: they don't use the wrapper library
# because the high level library (Converter and not FFMpeg) is not able to
# deal with these kind of args.

OPTIONS_OGG_EXCERPT = ['-ss','00:00:00.00', '-t', '180', '-acodec', 'libvorbis', '-vn', '-f', 'ogg']

OPTIONS_MP3_EXCERPT = ['-ss','00:00:00.00', '-t', '180', '-acodec', 'libmp3lame', '-vn', '-f', 'mp4']

class Command(BaseCommand):
    args = '<media_id media_id ...>'
    help = 'Encodes the specified media'

    def handle(self, *args, **options):

        # create directories if not exist
        # where audio/video files will be put
        directories = [archives_settings.STREAM_EXT_VIDEO_ROOT,
                       archives_settings.STREAM_INT_VIDEO_ROOT,
                       archives_settings.STREAM_EXT_AUDIO_ROOT,
                       archives_settings.STREAM_INT_AUDIO_ROOT]
        for directory in directories:
            if not os.path.exists(directory):
                os.makedirs(directory)

        self.converter = Converter()
        # loop inside command args to encode medias
        for media_id in args:
            # test if media exists
            try:
                media = Media.admin_objects.get(pk=int(media_id))
            except Media.DoesNotExist:
                raise CommandError('Media "%s" does not exist' % media_id)

            if media.media_type == 'video':
                self.encode_video(media)

            if media.media_type == 'audio':
                self.encode_audio(media)

            # Rare case were media_type is no set
            # FIXME: this should be remove after old archiprod is closed.
            if media.media_type is None:
                mimetype = mimetypes.guess_type(media.file.path)[0]
                if mimetype.startswith('video'):
                    self.encode_video(media)

                if mimetype.startswith('audio'):
                    self.encode_audio(media)

    def encode_video(self, media):
        """ Encode video """

        #pour les tests on force media.file
        #print settings.DATABASES
        #media.file = 'files/2013/12/19/video.mov'

        output_ext = os.path.join(archives_settings.STREAM_EXT_VIDEO_ROOT, str(media.file))
        output_int = os.path.join(archives_settings.STREAM_INT_VIDEO_ROOT, str(media.file))
        output_ext_dir = os.path.dirname(output_ext)
        output_int_dir = os.path.dirname(output_int)

        if not os.path.exists(output_ext_dir):
            os.makedirs(output_ext_dir)
        if not os.path.exists(output_int_dir):
            os.makedirs(output_int_dir)

        output_ext_ogg = output_ext+'.ogg'
        output_ext_webm = output_ext+'.webm'
        output_ext_mp4 = output_ext+'.mp4'
        output_ext_temp_mp4 = '/dev/null'

        output_int_ogg = output_int+'.ogg'
        output_int_webm = output_int+'.webm'
        output_int_mp4 = output_int+'.mp4'

        # FIXME: when webm will be available
        # add output_ext_mp4, output_int_mp4 and OPTIONS_MP4
        # for both ext and int encodings

        # For video, we first encode it in mp4
        # Then we encode webm and ogg from the mp4
        # And then symlink files ?!

        y_origin = int(media.size[1])
        if y_origin >= 720:
            OPTIONS_MP4_pass1.extend(['-vf', 'scale=-1:720'])

        self.ffmepgconvert(media.file.path, output_ext_temp_mp4, OPTIONS_MP4_pass1)
        self.ffmepgconvert(media.file.path, output_ext_mp4, OPTIONS_MP4_pass2)
        self.ffmepgconvert(output_ext_mp4, output_ext_ogg, OPTIONS_OGV)
        self.ffmepgconvert(output_ext_mp4, output_ext_webm, OPTIONS_WEBM)

        if not os.path.lexists(output_int_mp4):
            os.symlink(output_ext_mp4, output_int_mp4)

        if not os.path.lexists(output_int_ogg):
            os.symlink(output_ext_ogg, output_int_ogg)

        if not os.path.lexists(output_int_webm):
            os.symlink(output_ext_webm, output_int_webm)

        '''
        os.symlink(output_ext_mp4, output_int_mp4)
        os.symlink(output_ext_ogg, output_int_ogg)
        os.symlink(output_ext_webm, output_int_webm)
        '''

    def encode_audio(self, media):
        """ Encode audio """
        output_ext = os.path.join(archives_settings.STREAM_EXT_AUDIO_ROOT, str(media.file))
        output_int = os.path.join(archives_settings.STREAM_INT_AUDIO_ROOT, str(media.file))
        output_ext_dir = os.path.dirname(output_ext)
        output_int_dir = os.path.dirname(output_int)

        if not os.path.exists(output_ext_dir):
            os.makedirs(output_ext_dir)
        if not os.path.exists(output_int_dir):
            os.makedirs(output_int_dir)

        output_ext_ogg = output_ext+'.ogg'
        output_ext_mp3 = output_ext+'.mp3'

        output_int_ogg = output_int+'.ogg'
        output_int_mp3 = output_int+'.mp3'


        for param in zip([output_int_ogg, output_int_mp3],
                         [OPTIONS_OGG, OPTIONS_MP3]):
            self.convert(media.file.path, param[0], param[1])

        # For extern broadcast, we need to cut the media if it has a related work
        if media.work:
            # GOD SACEM RULE: 3 minutes OR 25% of media if duration < 12 minutes
            if media.duration < datetime.time(0, 12):
                duration = datetime.time(media.duration.hour/4, media.duration.minute/4, media.duration.second/4)
                duration_seconds = str(duration.minute*60 + duration.second)

                OPTIONS_OGG_EXCERPT[3] = duration_seconds
                OPTIONS_MP3_EXCERPT[3] = duration_seconds

            for param in zip([output_ext_ogg, output_ext_mp3],
                             [OPTIONS_OGG_EXCERPT, OPTIONS_MP3_EXCERPT]):
                # We use ffmepgconvert (see below) to convert this OPTIONS_OGG_EXCERPT
                # and OPTIONS_MP3_EXCERPT args.
                self.ffmepgconvert(media.file.path, param[0], param[1])
        else:
            # We just symlink the files
            os.symlink(output_int_ogg, output_ext_ogg)
            os.symlink(output_int_mp3, output_ext_mp3)



    def convert(self, file_in, file_out, options):
        """ Base converter wrapper for ffmpeg """
        conv = self.converter.convert(file_in, file_out, options, timeout=None)
        for timecode in conv:
            pass

    def ffmepgconvert(self, file_in, file_out, options):
        """ Base converter wrapper for ffmpeg with custom args
        Used to pass args for excerpts creation
        """
        conv = FFMpeg().convert(file_in, file_out, options, timeout=None)
        for timecode in conv:
            pass
