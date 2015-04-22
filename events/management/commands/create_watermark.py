# -*- coding: utf-8 -*-
from reportlab.pdfgen import canvas

from django.core.management.base import BaseCommand
from django.contrib.staticfiles import finders
from django.utils.encoding import force_text


class Command(BaseCommand):
    """
    Create watermark
    """
    text = '"watermark text"'
    help = 'Create a file watermark.pdf, used in `watermark` command'

    def handle(self, text="Ircam - Centre Pompidou", *args, **options):
        result = finders.find("pdf/watermark.pdf", all=False)
        watermark_path = force_text(result)

        c = canvas.Canvas(watermark_path) 
        c.setFont("Courier", 40)
        c.setFillGray(0.5,0.5)

        c.saveState() 
        c.translate(500,100) 
        c.rotate(45) 
        c.drawCentredString(0, 0, text) 
        c.drawCentredString(0, 300, text) 
        c.drawCentredString(0, 600, text) 
        c.restoreState() 
        c.save() 
