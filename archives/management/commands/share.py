# -*- coding: utf-8 -*-
import requests
import httplib
import httplib2
import os
import random
import sys
import time
import argparse

from optparse import make_option

from apiclient.discovery import build
from apiclient.errors import HttpError
from apiclient.http import MediaFileUpload
from oauth2client.file import Storage
from oauth2client.client import flow_from_clientsecrets, credentials_from_code
from oauth2client.tools import run, run_flow
from optparse import OptionParser

import soundcloud

from django.core.management.base import BaseCommand, CommandError

from archives.models import Media, Shared

# DAILYMOTION
DAILYMOTION_USERNAME = "api-test"
DAILYMOTION_PASSWORD = "ircam"
DAILYMOTION_API_KEY = '2b651fb5bf75f61074ea'
DAILYMOTION_API_SECRET_KEY = '90fe02aa3b7271327713440ade98d4898b408f18'

# SOUNDCLOUD
SOUNDCLOUD_USERNAME = "api-test"
SOUNDCLOUD_PASSWORD = "ircamtest"
SOUNDCLOUD_CLIENT_ID = '5034eebdb066ae37a5cd904ac77a6db5'
SOUNDCLOUD_CLIENT_SECRET = 'f25322524839f16dbac1eac926250579'


# YOUTUBE
YOUTUBE_CLIENT_ID = '616754054425'
YOUTUBE_CLIENT_SECRET = 'gNH2ugBV75Qc8uUIQNzo5KIP'

YOUTUBE_API_SERVICE_NAME = 'youtube'
YOUTUBE_API_VERSION = 'v3'

# VIMEO
VIMEO_USERNAME = 'api-test'
VIMEO_PASSWORD = 'ircamtest'
VIMEO_CLIENT_ID = 'f299eb873f48adf6a154815b65b1935e0df498ed'
VIMEO_CLIENT_SECRET = 'b11c23a3fc83e5685290ea58c66a5a84f99329ad'
VIMEO_ACCESS_TOKEN = 'e6b9d6c8b737e60abc1d7e2520dd254d'
VIMEO_ACCESS_TOKEN_SECRET = 'dfcdda1698f5f8558ee2ddde2cb8b620a37f479b'

RETRIABLE_STATUS_CODES = [500, 502, 503, 504]

RETRIABLE_EXCEPTIONS = (httplib2.HttpLib2Error, IOError, httplib.NotConnected,
  httplib.IncompleteRead, httplib.ImproperConnectionState,
  httplib.CannotSendRequest, httplib.CannotSendHeader,
  httplib.ResponseNotReady, httplib.BadStatusLine)



class Command(BaseCommand):
    args = '<media_id media_id ...>'
    help = 'Share media on web platforms'

    option_list = BaseCommand.option_list + (
            make_option('--delete',
                action='store_true',
                dest='delete',
                default=False,
                help='Delete shared medias'),
            make_option('--re-upload',
                action='store_true',
                dest='re-upload',
                default=False,
                help='Force re-upload of media files'),
            )

    def handle(self, *args, **options):

        if options['delete'] and options['re-upload']:
            raise CommandError('You can\'t do both delete and (set metadata or re-upload)')

        for media_id in args:
            try:
                media = Media.objects.get(pk=int(media_id))
            except Media.DoesNotExist:
                raise CommandError('Media "%s" does not exist' % media_id)

            try:
                Shared.objects.get(media=media)
            except Shared.DoesNotExist:
                if options['delete']:
                    raise CommandError('Share for media "%s" does not exist, you can\'t delete it' % media_id)
                if options['re-upload']:
                    raise CommandError('Share for media "%s" does not exist, you can\'t re-upload it' % media_id)

            if media.mime_type.startswith('video'):
                self.dailymotion(media, *args, **options)
            elif media.mime_type.startswith('audio'):
                self.soundcloud(media, *args, **options)  

            self.stdout.write('Successfully shared media "%s"' % media_id)

    def dailymotion(self, media, *args, **options):
        auth_data={'grant_type':'password', 
              'client_id':DAILYMOTION_API_KEY,
              'client_secret':DAILYMOTION_API_SECRET_KEY,
              'username':DAILYMOTION_USERNAME,
              'password':DAILYMOTION_PASSWORD,
              'scope':'manage_videos write delete'}
        r1 = requests.post("https://api.dailymotion.com/oauth/token", data=auth_data)

        token={'access_token':r1.json()['access_token']}
        # HACK, Dailymotion doesn't recognize /me until we reach it a first time as below:
        requests.get('https://api.dailymotion.com/me', params=token)

        # Test if media is already shared
        shared, created = Shared.objects.get_or_create(media=media)

        if not created and options['delete']:
            requests.delete("https://api.dailymotion.com/video/%s" % shared.dailymotion, params=token)
            shared.delete()
            return
        
        if options['re-upload'] or shared.dailymotion is None:
            r2 = requests.get("https://api.dailymotion.com/file/upload", params=token)
            files = {'file': open(media.file.path, 'rb')}
            r3 = requests.post(r2.json()['upload_url'], params=token, files=files)
            
            token_and_url = dict(token)
            token_and_url.update({'url':r3.json()['url']})
            r4 = requests.post('https://api.dailymotion.com/me/videos', params=token_and_url)
            shared.dailymotion = r4.json()['id']
            shared.save()

        # Fill dailymotion video with media metadatas
        title = media.__unicode__()
        if title == '':
            title = 'Sans titre'
        metadata = {'title':title, 'channel': 'creation', 'tags': 'ircam', 'published': 1}
        requests.post('https://api.dailymotion.com/video/%s' % shared.dailymotion, data=metadata, params=token)

    def soundcloud(self, media, *args, **options):
        # Create client object with app and user credentials
        client = soundcloud.Client(client_id=SOUNDCLOUD_CLIENT_ID,
                                   client_secret=SOUNDCLOUD_CLIENT_SECRET,
                                   username=SOUNDCLOUD_USERNAME,
                                   password=SOUNDCLOUD_PASSWORD)
        
        # Test if media is already shared
        shared, created = Shared.objects.get_or_create(media=media)
        if not created and options['delete']:
            track_id = shared.soundcloud
            # Delete the old one
            client.delete('/tracks/%s' % track_id)
            shared.delete()
            return

        title = media.__unicode__()
        if title == '':
            title = 'Sans titre'

        if options['re-upload'] or shared.soundcloud is None:
            # Create the track
            track = client.post('/tracks', track={
                'title': title,
                'asset_data': open(media.file.path, 'rb')
            })
            # Update our Shared instance
            shared.soundcloud = track.id
            shared.save()
        else:
            track = client.get('/tracks/%s' % shared.soundcloud)
            # update the track's metadata
            client.put(track.uri, track={
                'title': title,
                'asset_data': open(media.file.path, 'rb')
            })

    def vimeo(self, media, *args, **options):
        # see https://developer.vimeo.com/apis/advanced/upload
        pass

    '''
    def gen(self, media, *args, **options):
        from oauth2client.client import OAuth2WebServerFlow
        flow = OAuth2WebServerFlow(client_id=YOUTUBE_CLIENT_ID,
                                   client_secret=YOUTUBE_CLIENT_SECRET,
                                   scope='https://www.googleapis.com/auth/youtube.upload',
                                   redirect_uri='http://127.0.0.1:8000/auth_return')
        auth_uri = flow.step1_get_authorize_url()
        print auth_uri
        code =  raw_input('Enter verification code: ').strip()
        credentials = flow.step2_exchange(code)
        #print credentials
        #print credentials.to_json()

    def youtube(self, media):
        # scope = https://www.googleapis.com/auth/youtube.upload
        #credentials_from_code(client_id=YOUTUBE_CLIENT_ID, client_secret=YOUTUBE_CLIENT_SECRET,
        #                      scope="https://www.googleapis.com/auth/youtube.upload", code=)
        #pass
        import httplib2

        from oauth2client.file import Storage
        from apiclient.http import MediaFileUpload
        storage = Storage("credentials.json")
        credentials = storage.get()
        http = credentials.authorize(httplib2.Http())
        print credentials.invalid
        youtube = build(YOUTUBE_API_SERVICE_NAME, YOUTUBE_API_VERSION, http=http)
        print youtube
        tags = None

        title = media.__unicode__()
        if title == '':
            title = 'Sans titre'
        
        insert_request = youtube.videos().insert(
            part="snippet,status",
            body=dict(
              snippet=dict(
                title='title',
                description='media.summary',
                tags=tags,
                categoryId=22
              ),
              status=dict(
                privacyStatus="public"
              )
            ),
            # chunksize=-1 means that the entire file will be uploaded in a single
            # HTTP request. (If the upload fails, it will still be retried where it
            # left off.) This is usually a best practice, but if you're using Python
            # older than 2.6 or if you're running on App Engine, you should set the
            # chunksize to something like 1024 * 1024 (1 megabyte).
            media_body=MediaFileUpload(media.file.path, chunksize=-1, resumable=True)
        )
        response = None
        while response is None:
            print 'ok'
            print credentials.invalid
            status, response = insert_request.next_chunk()
        self.resumable_upload(insert_request, media)

    def resumable_upload(self, insert_request, media):
        response = None
        error = None
        retry = 0
        while response is None:
            try:
                print "Uploading file..."
                print insert_request
                status, response = insert_request.next_chunk()
                if 'id' in response:
                    print "'%s' (video id: %s) was successfully uploaded." % (
                    media.title, response['id'])
                else:
                    exit("The upload failed with an unexpected response: %s" % response)
            except HttpError, e:
                if e.resp.status in RETRIABLE_STATUS_CODES:
                    error = "A retriable HTTP error %d occurred:\n%s" % (e.resp.status,
                                                                         e.content)
                else:
                    raise
            except RETRIABLE_EXCEPTIONS, e:
                error = "A retriable error occurred: %s" % e

            if error is not None:
                print error
                retry += 1
                if retry > MAX_RETRIES:
                    exit("No longer attempting to retry.")

            max_sleep = 2 ** retry
            sleep_seconds = random.random() * max_sleep
            print "Sleeping %f seconds and then retrying..." % sleep_seconds
            time.sleep(sleep_seconds)


        #json = {"_module": "oauth2client.client", "token_expiry": "2013-11-21T12:51:56Z", "access_token": "ya29.1.AADtN_W7PQkiwOAKFs4tAFLy0i_i7DNcjzT5jac89Q4U2OUzvJomdyOkyLeJzUg", "token_uri": "https://accounts.google.com/o/oauth2/token", "invalid": false, "token_response": {"access_token": "ya29.1.AADtN_W7PQkiwOAKFs4tAFLy0i_i7DNcjzT5jac89Q4U2OUzvJomdyOkyLeJzUg", "token_type": "Bearer", "expires_in": 3596}, "client_id": "616754054425", "id_token": null, "client_secret": "gNH2ugBV75Qc8uUIQNzo5KIP", "revoke_uri": "https://accounts.google.com/o/oauth2/revoke", "_class": "OAuth2Credentials", "refresh_token": null, "user_agent": null}
        
    '''


