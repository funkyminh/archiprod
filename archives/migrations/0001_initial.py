# -*- coding: utf-8 -*-
import datetime
from south.db import db
from south.v2 import SchemaMigration
from django.db import models


class Migration(SchemaMigration):

    def forwards(self, orm):
        # Adding model 'Tag'
        db.create_table('archives_tag', (
            ('id', self.gf('django.db.models.fields.AutoField')(primary_key=True)),
            ('label', self.gf('django.db.models.fields.CharField')(max_length=255)),
            ('comment', self.gf('django.db.models.fields.TextField')(null=True, blank=True)),
            ('time_stamp', self.gf('django.db.models.fields.DateTimeField')(auto_now=True, blank=True)),
        ))
        db.send_create_signal('archives', ['Tag'])

        # Adding model 'Set'
        db.create_table('archives_set', (
            ('id', self.gf('django.db.models.fields.AutoField')(primary_key=True)),
            ('label', self.gf('django.db.models.fields.CharField')(max_length=255)),
            ('comment', self.gf('django.db.models.fields.CharField')(max_length=384, null=True, blank=True)),
            ('time_stamp', self.gf('django.db.models.fields.DateTimeField')(auto_now=True, blank=True)),
        ))
        db.send_create_signal('archives', ['Set'])

        # Adding model 'Archive'
        db.create_table('archives_archive', (
            ('id', self.gf('django.db.models.fields.CharField')(max_length=12, primary_key=True)),
            ('set', self.gf('django.db.models.fields.related.ForeignKey')(to=orm['archives.Set'], null=True, blank=True)),
            ('event', self.gf('django.db.models.fields.related.ForeignKey')(to=orm['events.Event'], null=True, blank=True)),
            ('title', self.gf('django.db.models.fields.CharField')(max_length=255, null=True, blank=True)),
            ('subtitle', self.gf('django.db.models.fields.CharField')(max_length=384, null=True, blank=True)),
            ('date', self.gf('django.db.models.fields.DateField')(null=True, blank=True)),
            ('comments', self.gf('django.db.models.fields.TextField')(null=True, blank=True)),
            ('summary', self.gf('django.db.models.fields.TextField')(null=True, blank=True)),
            ('time_stamp', self.gf('django.db.models.fields.DateTimeField')(auto_now=True, blank=True)),
            ('order', self.gf('django.db.models.fields.CharField')(default=None, max_length=12, null=True, blank=True)),
            ('user', self.gf('django.db.models.fields.related.ForeignKey')(to=orm['auth.User'], null=True, blank=True)),
            ('place', self.gf('django.db.models.fields.related.ForeignKey')(to=orm['utils.Place'], null=True, blank=True)),
            ('time', self.gf('django.db.models.fields.CharField')(default=None, max_length=5, null=True, blank=True)),
            ('old_id', self.gf('django.db.models.fields.CharField')(max_length=384, null=True, blank=True)),
            ('note2prog_id', self.gf('django.db.models.fields.CharField')(max_length=30, null=True, blank=True)),
            ('date_transfert', self.gf('django.db.models.fields.DateField')(null=True, blank=True)),
            ('available', self.gf('django.db.models.fields.CharField')(max_length=1, null=True, blank=True)),
            ('state', self.gf('django.db.models.fields.CharField')(max_length=1, null=True, blank=True)),
            ('pending', self.gf('django.db.models.fields.CharField')(max_length=1, null=True, blank=True)),
        ))
        db.send_create_signal('archives', ['Archive'])

        # Adding M2M table for field tags on 'Archive'
        db.create_table('archives_archive_tags', (
            ('id', models.AutoField(verbose_name='ID', primary_key=True, auto_created=True)),
            ('archive', models.ForeignKey(orm['archives.archive'], null=False)),
            ('tag', models.ForeignKey(orm['archives.tag'], null=False))
        ))
        db.create_unique('archives_archive_tags', ['archive_id', 'tag_id'])

        # Adding M2M table for field collectivities on 'Archive'
        db.create_table('archives_archive_collectivities', (
            ('id', models.AutoField(verbose_name='ID', primary_key=True, auto_created=True)),
            ('archive', models.ForeignKey(orm['archives.archive'], null=False)),
            ('collectivity', models.ForeignKey(orm['utils.collectivity'], null=False))
        ))
        db.create_unique('archives_archive_collectivities', ['archive_id', 'collectivity_id'])

        # Adding model 'Media'
        db.create_table('archives_media', (
            ('id', self.gf('django.db.models.fields.AutoField')(primary_key=True)),
            ('media', self.gf('django.db.models.fields.CharField')(max_length=36)),
            ('order', self.gf('django.db.models.fields.IntegerField')(null=True, blank=True)),
            ('archive', self.gf('django.db.models.fields.related.ForeignKey')(to=orm['archives.Archive'], null=True, blank=True)),
            ('title', self.gf('django.db.models.fields.CharField')(max_length=255, null=True, blank=True)),
            ('duration', self.gf('django.db.models.fields.CharField')(max_length=12, null=True, blank=True)),
            ('comments', self.gf('django.db.models.fields.TextField')(null=True, blank=True)),
            ('time_stamp', self.gf('django.db.models.fields.DateTimeField')(auto_now=True, blank=True)),
            ('work', self.gf('django.db.models.fields.related.ForeignKey')(to=orm['utils.Work'], null=True, blank=True)),
            ('publisher', self.gf('django.db.models.fields.related.ForeignKey')(blank=True, related_name='publisher', null=True, to=orm['utils.Collectivity'])),
            ('confidentiality', self.gf('django.db.models.fields.CharField')(max_length=1, null=True, blank=True)),
            ('file', self.gf('django.db.models.fields.files.FileField')(max_length=1000, null=True, blank=True)),
            ('file_ext', self.gf('django.db.models.fields.files.FileField')(max_length=100, null=True, blank=True)),
            ('file_int', self.gf('django.db.models.fields.files.FileField')(max_length=100, null=True, blank=True)),
            ('record_type', self.gf('django.db.models.fields.CharField')(max_length=1, null=True, blank=True)),
            ('summary', self.gf('django.db.models.fields.TextField')(null=True, blank=True)),
            ('mime_type', self.gf('django.db.models.fields.CharField')(max_length=192, null=True, blank=True)),
            ('user', self.gf('django.db.models.fields.related.ForeignKey')(to=orm['auth.User'], null=True, blank=True)),
        ))
        db.send_create_signal('archives', ['Media'])

        # Adding M2M table for field collectivities on 'Media'
        db.create_table('archives_media_collectivities', (
            ('id', models.AutoField(verbose_name='ID', primary_key=True, auto_created=True)),
            ('media', models.ForeignKey(orm['archives.media'], null=False)),
            ('collectivity', models.ForeignKey(orm['utils.collectivity'], null=False))
        ))
        db.create_unique('archives_media_collectivities', ['media_id', 'collectivity_id'])

        # Adding model 'Contract'
        db.create_table('archives_contract', (
            ('id', self.gf('django.db.models.fields.AutoField')(primary_key=True)),
            ('title', self.gf('django.db.models.fields.CharField')(max_length=255)),
            ('archive', self.gf('django.db.models.fields.related.ForeignKey')(to=orm['archives.Archive'])),
            ('comments', self.gf('django.db.models.fields.TextField')(null=True, blank=True)),
            ('nb_pages', self.gf('django.db.models.fields.IntegerField')(null=True, blank=True)),
            ('user', self.gf('django.db.models.fields.related.ForeignKey')(to=orm['auth.User'])),
            ('time_stamp', self.gf('django.db.models.fields.DateTimeField')(auto_now=True, blank=True)),
            ('file', self.gf('django.db.models.fields.files.FileField')(max_length=100, null=True, blank=True)),
        ))
        db.send_create_signal('archives', ['Contract'])

        # Adding model 'ArchiveParticipant'
        db.create_table('archives_archiveparticipant', (
            ('id', self.gf('django.db.models.fields.AutoField')(primary_key=True)),
            ('archive', self.gf('django.db.models.fields.related.ForeignKey')(to=orm['archives.Archive'])),
            ('person', self.gf('django.db.models.fields.related.ForeignKey')(to=orm['utils.Person'])),
            ('role', self.gf('django.db.models.fields.related.ForeignKey')(to=orm['utils.Role'])),
        ))
        db.send_create_signal('archives', ['ArchiveParticipant'])

        # Adding model 'Participant'
        db.create_table('archives_participant', (
            ('id', self.gf('django.db.models.fields.AutoField')(primary_key=True)),
            ('media', self.gf('django.db.models.fields.related.ForeignKey')(to=orm['archives.Media'])),
            ('person', self.gf('django.db.models.fields.related.ForeignKey')(to=orm['utils.Person'])),
            ('role', self.gf('django.db.models.fields.related.ForeignKey')(to=orm['utils.Role'])),
        ))
        db.send_create_signal('archives', ['Participant'])


    def backwards(self, orm):
        # Deleting model 'Tag'
        db.delete_table('archives_tag')

        # Deleting model 'Set'
        db.delete_table('archives_set')

        # Deleting model 'Archive'
        db.delete_table('archives_archive')

        # Removing M2M table for field tags on 'Archive'
        db.delete_table('archives_archive_tags')

        # Removing M2M table for field collectivities on 'Archive'
        db.delete_table('archives_archive_collectivities')

        # Deleting model 'Media'
        db.delete_table('archives_media')

        # Removing M2M table for field collectivities on 'Media'
        db.delete_table('archives_media_collectivities')

        # Deleting model 'Contract'
        db.delete_table('archives_contract')

        # Deleting model 'ArchiveParticipant'
        db.delete_table('archives_archiveparticipant')

        # Deleting model 'Participant'
        db.delete_table('archives_participant')


    models = {
        'archives.archive': {
            'Meta': {'object_name': 'Archive'},
            'available': ('django.db.models.fields.CharField', [], {'max_length': '1', 'null': 'True', 'blank': 'True'}),
            'collectivities': ('django.db.models.fields.related.ManyToManyField', [], {'symmetrical': 'False', 'to': "orm['utils.Collectivity']", 'null': 'True', 'blank': 'True'}),
            'comments': ('django.db.models.fields.TextField', [], {'null': 'True', 'blank': 'True'}),
            'date': ('django.db.models.fields.DateField', [], {'null': 'True', 'blank': 'True'}),
            'date_transfert': ('django.db.models.fields.DateField', [], {'null': 'True', 'blank': 'True'}),
            'event': ('django.db.models.fields.related.ForeignKey', [], {'to': "orm['events.Event']", 'null': 'True', 'blank': 'True'}),
            'id': ('django.db.models.fields.CharField', [], {'max_length': '12', 'primary_key': 'True'}),
            'note2prog_id': ('django.db.models.fields.CharField', [], {'max_length': '30', 'null': 'True', 'blank': 'True'}),
            'old_id': ('django.db.models.fields.CharField', [], {'max_length': '384', 'null': 'True', 'blank': 'True'}),
            'order': ('django.db.models.fields.CharField', [], {'default': 'None', 'max_length': '12', 'null': 'True', 'blank': 'True'}),
            'participants': ('django.db.models.fields.related.ManyToManyField', [], {'symmetrical': 'False', 'to': "orm['utils.Person']", 'null': 'True', 'through': "orm['archives.ArchiveParticipant']", 'blank': 'True'}),
            'pending': ('django.db.models.fields.CharField', [], {'max_length': '1', 'null': 'True', 'blank': 'True'}),
            'place': ('django.db.models.fields.related.ForeignKey', [], {'to': "orm['utils.Place']", 'null': 'True', 'blank': 'True'}),
            'set': ('django.db.models.fields.related.ForeignKey', [], {'to': "orm['archives.Set']", 'null': 'True', 'blank': 'True'}),
            'state': ('django.db.models.fields.CharField', [], {'max_length': '1', 'null': 'True', 'blank': 'True'}),
            'subtitle': ('django.db.models.fields.CharField', [], {'max_length': '384', 'null': 'True', 'blank': 'True'}),
            'summary': ('django.db.models.fields.TextField', [], {'null': 'True', 'blank': 'True'}),
            'tags': ('django.db.models.fields.related.ManyToManyField', [], {'symmetrical': 'False', 'to': "orm['archives.Tag']", 'null': 'True', 'blank': 'True'}),
            'time': ('django.db.models.fields.CharField', [], {'default': 'None', 'max_length': '5', 'null': 'True', 'blank': 'True'}),
            'time_stamp': ('django.db.models.fields.DateTimeField', [], {'auto_now': 'True', 'blank': 'True'}),
            'title': ('django.db.models.fields.CharField', [], {'max_length': '255', 'null': 'True', 'blank': 'True'}),
            'user': ('django.db.models.fields.related.ForeignKey', [], {'to': "orm['auth.User']", 'null': 'True', 'blank': 'True'})
        },
        'archives.archiveparticipant': {
            'Meta': {'object_name': 'ArchiveParticipant'},
            'archive': ('django.db.models.fields.related.ForeignKey', [], {'to': "orm['archives.Archive']"}),
            'id': ('django.db.models.fields.AutoField', [], {'primary_key': 'True'}),
            'person': ('django.db.models.fields.related.ForeignKey', [], {'to': "orm['utils.Person']"}),
            'role': ('django.db.models.fields.related.ForeignKey', [], {'to': "orm['utils.Role']"})
        },
        'archives.contract': {
            'Meta': {'object_name': 'Contract'},
            'archive': ('django.db.models.fields.related.ForeignKey', [], {'to': "orm['archives.Archive']"}),
            'comments': ('django.db.models.fields.TextField', [], {'null': 'True', 'blank': 'True'}),
            'file': ('django.db.models.fields.files.FileField', [], {'max_length': '100', 'null': 'True', 'blank': 'True'}),
            'id': ('django.db.models.fields.AutoField', [], {'primary_key': 'True'}),
            'nb_pages': ('django.db.models.fields.IntegerField', [], {'null': 'True', 'blank': 'True'}),
            'time_stamp': ('django.db.models.fields.DateTimeField', [], {'auto_now': 'True', 'blank': 'True'}),
            'title': ('django.db.models.fields.CharField', [], {'max_length': '255'}),
            'user': ('django.db.models.fields.related.ForeignKey', [], {'to': "orm['auth.User']"})
        },
        'archives.media': {
            'Meta': {'object_name': 'Media'},
            'archive': ('django.db.models.fields.related.ForeignKey', [], {'to': "orm['archives.Archive']", 'null': 'True', 'blank': 'True'}),
            'collectivities': ('django.db.models.fields.related.ManyToManyField', [], {'symmetrical': 'False', 'to': "orm['utils.Collectivity']", 'null': 'True', 'blank': 'True'}),
            'comments': ('django.db.models.fields.TextField', [], {'null': 'True', 'blank': 'True'}),
            'confidentiality': ('django.db.models.fields.CharField', [], {'max_length': '1', 'null': 'True', 'blank': 'True'}),
            'duration': ('django.db.models.fields.CharField', [], {'max_length': '12', 'null': 'True', 'blank': 'True'}),
            'file': ('django.db.models.fields.files.FileField', [], {'max_length': '100', 'null': 'True', 'blank': 'True'}),
            'file_ext': ('django.db.models.fields.files.FileField', [], {'max_length': '100', 'null': 'True', 'blank': 'True'}),
            'file_int': ('django.db.models.fields.files.FileField', [], {'max_length': '100', 'null': 'True', 'blank': 'True'}),
            'id': ('django.db.models.fields.AutoField', [], {'primary_key': 'True'}),
            'media': ('django.db.models.fields.CharField', [], {'max_length': '36'}),
            'mime_type': ('django.db.models.fields.CharField', [], {'max_length': '192', 'null': 'True', 'blank': 'True'}),
            'order': ('django.db.models.fields.IntegerField', [], {'null': 'True', 'blank': 'True'}),
            'participants': ('django.db.models.fields.related.ManyToManyField', [], {'symmetrical': 'False', 'to': "orm['utils.Person']", 'null': 'True', 'through': "orm['archives.Participant']", 'blank': 'True'}),
            'publisher': ('django.db.models.fields.related.ForeignKey', [], {'blank': 'True', 'related_name': "'publisher'", 'null': 'True', 'to': "orm['utils.Collectivity']"}),
            'record_type': ('django.db.models.fields.CharField', [], {'max_length': '1', 'null': 'True', 'blank': 'True'}),
            'summary': ('django.db.models.fields.TextField', [], {'null': 'True', 'blank': 'True'}),
            'time_stamp': ('django.db.models.fields.DateTimeField', [], {'auto_now': 'True', 'blank': 'True'}),
            'title': ('django.db.models.fields.CharField', [], {'max_length': '255', 'null': 'True', 'blank': 'True'}),
            'user': ('django.db.models.fields.related.ForeignKey', [], {'to': "orm['auth.User']", 'null': 'True', 'blank': 'True'}),
            'work': ('django.db.models.fields.related.ForeignKey', [], {'to': "orm['utils.Work']", 'null': 'True', 'blank': 'True'})
        },
        'archives.participant': {
            'Meta': {'object_name': 'Participant'},
            'id': ('django.db.models.fields.AutoField', [], {'primary_key': 'True'}),
            'media': ('django.db.models.fields.related.ForeignKey', [], {'to': "orm['archives.Media']"}),
            'person': ('django.db.models.fields.related.ForeignKey', [], {'to': "orm['utils.Person']"}),
            'role': ('django.db.models.fields.related.ForeignKey', [], {'to': "orm['utils.Role']"})
        },
        'archives.set': {
            'Meta': {'object_name': 'Set'},
            'comment': ('django.db.models.fields.CharField', [], {'max_length': '384', 'null': 'True', 'blank': 'True'}),
            'id': ('django.db.models.fields.AutoField', [], {'primary_key': 'True'}),
            'label': ('django.db.models.fields.CharField', [], {'max_length': '255'}),
            'time_stamp': ('django.db.models.fields.DateTimeField', [], {'auto_now': 'True', 'blank': 'True'})
        },
        'archives.tag': {
            'Meta': {'object_name': 'Tag'},
            'comment': ('django.db.models.fields.TextField', [], {'null': 'True', 'blank': 'True'}),
            'id': ('django.db.models.fields.AutoField', [], {'primary_key': 'True'}),
            'label': ('django.db.models.fields.CharField', [], {'max_length': '255'}),
            'time_stamp': ('django.db.models.fields.DateTimeField', [], {'auto_now': 'True', 'blank': 'True'})
        },
        'auth.group': {
            'Meta': {'object_name': 'Group'},
            'id': ('django.db.models.fields.AutoField', [], {'primary_key': 'True'}),
            'name': ('django.db.models.fields.CharField', [], {'unique': 'True', 'max_length': '80'}),
            'permissions': ('django.db.models.fields.related.ManyToManyField', [], {'to': "orm['auth.Permission']", 'symmetrical': 'False', 'blank': 'True'})
        },
        'auth.permission': {
            'Meta': {'ordering': "('content_type__app_label', 'content_type__model', 'codename')", 'unique_together': "(('content_type', 'codename'),)", 'object_name': 'Permission'},
            'codename': ('django.db.models.fields.CharField', [], {'max_length': '100'}),
            'content_type': ('django.db.models.fields.related.ForeignKey', [], {'to': "orm['contenttypes.ContentType']"}),
            'id': ('django.db.models.fields.AutoField', [], {'primary_key': 'True'}),
            'name': ('django.db.models.fields.CharField', [], {'max_length': '50'})
        },
        'auth.user': {
            'Meta': {'object_name': 'User'},
            'date_joined': ('django.db.models.fields.DateTimeField', [], {'default': 'datetime.datetime.now'}),
            'email': ('django.db.models.fields.EmailField', [], {'max_length': '75', 'blank': 'True'}),
            'first_name': ('django.db.models.fields.CharField', [], {'max_length': '30', 'blank': 'True'}),
            'groups': ('django.db.models.fields.related.ManyToManyField', [], {'to': "orm['auth.Group']", 'symmetrical': 'False', 'blank': 'True'}),
            'id': ('django.db.models.fields.AutoField', [], {'primary_key': 'True'}),
            'is_active': ('django.db.models.fields.BooleanField', [], {'default': 'True'}),
            'is_staff': ('django.db.models.fields.BooleanField', [], {'default': 'False'}),
            'is_superuser': ('django.db.models.fields.BooleanField', [], {'default': 'False'}),
            'last_login': ('django.db.models.fields.DateTimeField', [], {'default': 'datetime.datetime.now'}),
            'last_name': ('django.db.models.fields.CharField', [], {'max_length': '30', 'blank': 'True'}),
            'password': ('django.db.models.fields.CharField', [], {'max_length': '128'}),
            'user_permissions': ('django.db.models.fields.related.ManyToManyField', [], {'to': "orm['auth.Permission']", 'symmetrical': 'False', 'blank': 'True'}),
            'username': ('django.db.models.fields.CharField', [], {'unique': 'True', 'max_length': '30'})
        },
        'contenttypes.contenttype': {
            'Meta': {'ordering': "('name',)", 'unique_together': "(('app_label', 'model'),)", 'object_name': 'ContentType', 'db_table': "'django_content_type'"},
            'app_label': ('django.db.models.fields.CharField', [], {'max_length': '100'}),
            'id': ('django.db.models.fields.AutoField', [], {'primary_key': 'True'}),
            'model': ('django.db.models.fields.CharField', [], {'max_length': '100'}),
            'name': ('django.db.models.fields.CharField', [], {'max_length': '100'})
        },
        'events.event': {
            'Meta': {'ordering': "['tree_id', 'lft']", 'object_name': 'Event'},
            'date_end': ('django.db.models.fields.DateField', [], {'null': 'True', 'blank': 'True'}),
            'date_start': ('django.db.models.fields.DateField', [], {'null': 'True', 'blank': 'True'}),
            'event_type': ('django.db.models.fields.related.ForeignKey', [], {'to': "orm['events.EventType']", 'null': 'True', 'blank': 'True'}),
            'id': ('django.db.models.fields.AutoField', [], {'primary_key': 'True'}),
            'level': ('django.db.models.fields.PositiveIntegerField', [], {'db_index': 'True'}),
            'lft': ('django.db.models.fields.PositiveIntegerField', [], {'db_index': 'True'}),
            'parent': ('mptt.fields.TreeForeignKey', [], {'blank': 'True', 'related_name': "'children'", 'null': 'True', 'to': "orm['events.Event']"}),
            'rght': ('django.db.models.fields.PositiveIntegerField', [], {'db_index': 'True'}),
            'subtitle': ('django.db.models.fields.CharField', [], {'max_length': '384', 'null': 'True', 'blank': 'True'}),
            'time_stamp': ('django.db.models.fields.DateTimeField', [], {'auto_now': 'True', 'blank': 'True'}),
            'title': ('django.db.models.fields.CharField', [], {'max_length': '255'}),
            'tree_id': ('django.db.models.fields.PositiveIntegerField', [], {'db_index': 'True'})
        },
        'events.eventtype': {
            'Meta': {'object_name': 'EventType'},
            'id': ('django.db.models.fields.AutoField', [], {'primary_key': 'True'}),
            'label': ('django.db.models.fields.CharField', [], {'max_length': '255'})
        },
        'utils.collectivity': {
            'Meta': {'object_name': 'Collectivity'},
            'id': ('django.db.models.fields.AutoField', [], {'primary_key': 'True'}),
            'name': ('django.db.models.fields.CharField', [], {'max_length': '255'})
        },
        'utils.composer': {
            'Meta': {'object_name': 'Composer'},
            'id': ('django.db.models.fields.AutoField', [], {'primary_key': 'True'}),
            'person': ('django.db.models.fields.related.ForeignKey', [], {'to': "orm['utils.Person']"}),
            'role': ('django.db.models.fields.related.ForeignKey', [], {'to': "orm['utils.Role']"}),
            'work': ('django.db.models.fields.related.ForeignKey', [], {'to': "orm['utils.Work']"})
        },
        'utils.person': {
            'Meta': {'object_name': 'Person'},
            'first_name': ('django.db.models.fields.CharField', [], {'max_length': '150'}),
            'id': ('django.db.models.fields.AutoField', [], {'primary_key': 'True'}),
            'last_name': ('django.db.models.fields.CharField', [], {'max_length': '150'})
        },
        'utils.place': {
            'Meta': {'object_name': 'Place'},
            'city': ('django.db.models.fields.CharField', [], {'max_length': '765'}),
            'country': ('django.db.models.fields.CharField', [], {'max_length': '765'}),
            'hall': ('django.db.models.fields.CharField', [], {'max_length': '255', 'null': 'True', 'blank': 'True'}),
            'id': ('django.db.models.fields.AutoField', [], {'primary_key': 'True'}),
            'name': ('django.db.models.fields.CharField', [], {'max_length': '255'})
        },
        'utils.role': {
            'Meta': {'object_name': 'Role'},
            'id': ('django.db.models.fields.AutoField', [], {'primary_key': 'True'}),
            'label': ('django.db.models.fields.CharField', [], {'max_length': '255'})
        },
        'utils.work': {
            'Meta': {'object_name': 'Work'},
            'composers': ('django.db.models.fields.related.ManyToManyField', [], {'symmetrical': 'False', 'to': "orm['utils.Person']", 'null': 'True', 'through': "orm['utils.Composer']", 'blank': 'True'}),
            'id': ('django.db.models.fields.AutoField', [], {'primary_key': 'True'}),
            'subtitle': ('django.db.models.fields.CharField', [], {'max_length': '384', 'null': 'True', 'blank': 'True'}),
            'title': ('django.db.models.fields.CharField', [], {'max_length': '384'}),
            'year': ('django.db.models.fields.CharField', [], {'max_length': '12', 'null': 'True', 'blank': 'True'})
        }
    }

    complete_apps = ['archives']