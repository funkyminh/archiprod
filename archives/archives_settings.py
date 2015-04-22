# -*- coding: utf-8 -*-
import os
from django.conf import settings

"""
Define settings for video and audio stream url and path
"""

STREAM_EXT_ROOT = os.path.join(settings.STREAM_ROOT, 'ext')
STREAM_INT_ROOT = os.path.join(settings.STREAM_ROOT, 'int')

STREAM_EXT_URL = os.path.join(settings.STREAM_URL, 'ext')
STREAM_INT_URL = os.path.join(settings.STREAM_URL, 'int')

STREAM_EXT_AUDIO_ROOT = os.path.join(STREAM_EXT_ROOT, 'audio')
STREAM_EXT_VIDEO_ROOT = os.path.join(STREAM_EXT_ROOT, 'video')
STREAM_INT_AUDIO_ROOT = os.path.join(STREAM_INT_ROOT, 'audio')
STREAM_INT_VIDEO_ROOT = os.path.join(STREAM_INT_ROOT, 'video')

STREAM_EXT_AUDIO_URL = os.path.join(STREAM_EXT_URL, 'audio')
STREAM_EXT_VIDEO_URL = os.path.join(STREAM_EXT_URL, 'video')
STREAM_INT_AUDIO_URL = os.path.join(STREAM_INT_URL, 'audio')
STREAM_INT_VIDEO_URL = os.path.join(STREAM_INT_URL, 'video')