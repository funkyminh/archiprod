# -*- coding: utf-8 -*-
from PyPDF2 import PdfFileWriter, PdfFileReader

from django.core.management.base import BaseCommand
from django.contrib.staticfiles import finders
from django.utils.encoding import force_text

from events.models import ProgramNote


class Command(BaseCommand):
    """
    Watermark pdf with a copyright
    """
    args = '<programnote_id programnote_id ...>'
    help = 'Watermarks the specified program note'

    def handle(self, *args, **options):
        result = finders.find("pdf/watermark.pdf", all=False)
        watermark_path = force_text(result)
        self.watermark_file = PdfFileReader(open(watermark_path, "rb")).getPage(0)
        for programnote_id in args:
            program_note = ProgramNote.objects.get(id=programnote_id)
            self.watermark(program_note)

    def watermark(self, program_note):
        output = PdfFileWriter()
        input_file = PdfFileReader(open(program_note.program.path, "rb"))
        nb_of_pages = input_file.getNumPages()

        for i in range(nb_of_pages):
            current_page = input_file.getPage(i)
            current_page.mergePage(self.watermark_file)
            output.addPage(current_page)

        outputStream = file("%s-wm.pdf" % program_note.program.path[:-4], "wb")
        output.write(outputStream)
        outputStream.close()

