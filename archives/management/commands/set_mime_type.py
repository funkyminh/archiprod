# -*- coding: utf-8 -*-
import mimetypes
import os
from django.core.management.base import BaseCommand

from archives.models import Media

class Command(BaseCommand):
    args = None
    help = 'Set the mime_type of all media with an available media file'

    def handle(self, *args, **options):
        medias = Media.objects.all()
        for media in medias:
            if media.file:
                if os.path.exists(media.file.path):
                    media.mime_type = mimetypes.guess_type(media.file.path)[0]
                    media.save()
                else:
                    print 'Need to fix media: %s - %s' % (media, media.id)