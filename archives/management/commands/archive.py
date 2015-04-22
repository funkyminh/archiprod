# -*- coding: utf-8 -*-
import os
import datetime
import shutil

from django.conf import settings
from django.core.management.base import BaseCommand
from django.utils.encoding import force_str, force_text

from archives.models import Media

class Command(BaseCommand):
    args = '<path> <media_id>'
    help = 'Archive the specified path, and create a Media instance'

    def handle(self, *args, **options):
        file_path = args[0]
        media_id = args[1]
        prefix = settings.FTP_ROOT
        path = os.path.join(prefix, file_path)
        # Build target directory, and paths
        destination_tmpl = os.path.join(settings.MEDIA_ROOT, 'files/%Y/%m/%d')
        destination = os.path.normpath(force_text(datetime.datetime.now().strftime(force_str(destination_tmpl))))
        try:
            os.makedirs(destination)
        except OSError:
            pass
        rel_path = force_text(datetime.datetime.now().strftime('files/%Y/%m/%d/'+os.path.basename(file_path)))
        shutil.move(path, os.path.join(destination, os.path.basename(file_path)))
        # Save media instance
        if media_id is None:
            media = Media()
        else:
            media = Media.objects.get(id=media_id)
        media.file.name = rel_path
        media.confidentiality = '2'
        media.save()
