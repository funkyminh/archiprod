# -*- coding: utf-8 -*-
from django import template

register = template.Library()


@register.inclusion_tag('archives/media_element.html', takes_context=True)
def video_player(context, media):
    # We need to 'remind' our video_player tag to have
    # 'in_situ' value available (this value come from request context).
    ct = {'url': None,
          'type': None,
          'in_situ':context['in_situ'],
          'site':context['site']}
    try:
        # case where file is migrated
        # must return an html5 media player
        ct['url'] = media.file.url
        ct['media'] = media
        ct['type'] = 'new_archiprod_media'
    except:
        # case where file isn't migrated
        # so we need to play using old system
        if media.media.startswith('AU'):
            # this is an audio file
            # prefix = 'rtmp://streams.mediatheque.ircam.fr/internet'
            prefix = 'http://archiprod.ircam.fr/get_audio.php?file='
            ct['type'] = 'audio_extern'
            if len(media.media) == 11:
                base = media.media[0:9]+media.media[10:]
            else:
                base = media.media[0:8]+media.media[10:]
            ct['url'] = '%s%s.aiff' % (prefix, base)
            ct['base'] = media.media[0:10]
            ct['index'] = media.media[10:]
        else:
            # this is a video file
            ct['type'] = 'video_extern'
            prefix = 'http://archiprod-externe.ircam.fr/video'
            ct['url'] = '%s/%s.mp4' % (prefix, media.media)
    return ct
