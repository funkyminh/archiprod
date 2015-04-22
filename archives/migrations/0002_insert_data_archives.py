# -*- coding: utf-8 -*-
import datetime
from south.db import db
from south.v2 import DataMigration
from django.db import models
from django.db import connection, transaction

class Migration(DataMigration):

    def forwards(self, orm):

        cursor1 = connection.cursor()
        cursor1.execute("insert into `archives_tag`(`comment`, `id`, `label`, `time_stamp`) select t2.`sous_titre`, t2.`id`, t2.`intitule`, t2.`time_stamp` from `tag_evenement` as t2")

        cursor2 = connection.cursor()
        cursor2.execute("insert into `archives_set` (`comment`, `id`, `label`, `time_stamp`) select t2.`sous_titre`, t2.`id`, t2.`intitule`, t2.`time_stamp` from `evenement` as t2")

        cursor3 = connection.cursor()
        cursor3.execute("insert into `archives_contract` (`archive_id`, `comments`, `file`, `id`, `nb_pages`, `time_stamp`, `title`, `user_id`) select t2.`parent_id`, t2.`notes`, t2.`contract`, t2.`id`, t2.`num_pages`, t2.`time_stamp`, t2.`intitule`, t2.`technicien_id` from `contrat` as t2")

        cursor4 = connection.cursor()
        cursor4.execute("insert into `archives_archiveparticipant` (`archive_id`, `person_id`, `role_id`) select t2.`video_volume_id`, t2.`personne_id`, t2.`role_id` from `video_volume_personne_role` as t2")

        cursor5 = connection.cursor()
        cursor5.execute("insert into `archives_participant` (`media_id`, `person_id`, `role_id`) select t2.`video_record_id`, t2.`personne_id`, t2.`role_id` from `video_record_personne_role` as t2")

        '''
        #TO VERIFY
        insert into `archives_archiveparticipant`
        (`archive_id`, `person_id`, `role_id`)
        select t2.`volume_id`, t2.`personne_id`, t2.`role_id`
        from `volume_personne_role` as t2;

        #TO VERIFY
        insert into `archives_participant`
        (`media_id`, `person_id`, `role_id`)
        select t2.`partie_id`, t2.`personne_id`, t2.`role_id`
        from `partie_personne_role` as t2;
        '''

        #cursor17 = connection.cursor()
        #cursor17.execute("insert into `archives_archiveparticipant` (`archive_id`, `person_id`, `role_id`) select t2.`volume_id`, t2.`personne_id`, t2.`role_id` from `volume_personne_role` as t2")

        #cursor18 = connection.cursor()
        #cursor18.execute("insert into `archives_participant` (`media_id`, `person_id`, `role_id`) select t2.`partie_id`, t2.`personne_id`, t2.`role_id` from `partie_personne_role` as t2")

        cursor6 = connection.cursor()
        cursor6.execute("insert into `archives_archive` (`available`, `comments`, `date`, `date_transfert`, `event_id`, `id`, `note2prog_id`, `old_id`, `order`, `pending`, `place_id`, `set_id`, `state`, `subtitle`, `summary`, `time`, `time_stamp`, `title`, `user_id`) select NULL, t2.`notes`, t2.`date`, NULL, t2.`evenement2_id`, t2.`id`, NULL, NULL, t2.`sort`, NULL, t2.`lieu_id`, t2.`parent_id`, NULL, t2.`sous_titre`, t2.`resume`, t2.`horaire`, t2.`time_stamp`, t2.`intitule`, t2.`technicien_id` from `video_volume` as t2")

        cursor7 = connection.cursor()
        cursor7.execute("insert into `archives_archive` (`available`, `comments`, `date`, `date_transfert`, `event_id`, `id`, `note2prog_id`, `old_id`, `order`, `pending`, `place_id`, `set_id`, `state`, `subtitle`, `summary`, `time`, `time_stamp`, `title`, `user_id`) select t2.`pret`, t2.`notes`, t2.`date`, t2.`date_transfert`, t2.`evenement2_id`, t2.`id`, t2.`note2prog_id`, t2.`old_id`, NULL, t2.`pending`, t2.`lieu_id`, t2.`parent_id`, NULL, t2.`sous_titre`, t2.`resume`, t2.`horaire`, t2.`time_stamp`, t2.`intitule`, t2.`technicien_id` from `volume` as t2")

        cursor8 = connection.cursor()
        #cursor8.execute("insert into `archives_media` (`archive_id`, `comments`, `confidentiality`, `duration`, `file`, `file_ext`, `file_int`, `media`, `mime_type`, `order`, `publisher_id`, `record_type`, `summary`, `time_stamp`, `title`, `user_id`, `work_id`) select t2.`parent_id`, t2.`notes`, t2.`confidentialite_record`, t2.`duree`, t2.`video`, t2.`video_ext`, t2.`video_int`, CONCAT(t2.`parent_id`, '-', t2.`id`), t2.`mime_type`, NULL, NULL, t2.`type_record`, t2.`resume`, t2.`time_stamp`, t2.`intitule`, t2.`technicien_id`, NULL from `video_record` as t2")
        cursor8.execute("insert into `archives_media` (`id`, `archive_id`, `comments`, `confidentiality`, `duration`, `file`, `file_ext`, `file_int`, `media`, `mime_type`, `order`, `publisher_id`, `record_type`, `summary`, `time_stamp`, `title`, `user_id`, `work_id`) select t2.`id`, t2.`parent_id`, t2.`notes`, t2.`confidentialite_record`, t2.`duree`, t2.`video`, t2.`video_ext`, t2.`video_int`, CONCAT(t2.`parent_id`, '-', t2.`id`), t2.`mime_type`, NULL, NULL, t2.`type_record`, t2.`resume`, t2.`time_stamp`, t2.`intitule`, t2.`technicien_id`, NULL from `video_record` as t2")

        cursor9 = connection.cursor()
        cursor9.execute("insert into `archives_media` (`archive_id`, `comments`, `confidentiality`, `duration`, `file`, `file_ext`, `file_int`, `media`, `mime_type`, `order`, `publisher_id`, `record_type`, `summary`, `time_stamp`, `title`, `user_id`, `work_id`) select t2.`volume_id`, t2.`notes`, t2.`confidentialite_partie`, t2.`duree`, t2.`audio`, t2.`audio_ext`, t2.`audio_int`,  CONCAT(t2.`volume_id`, t2.`seq`), NULL, t2.`seq`, t2.`editeur_partition_id`, NULL, NULL, t2.`time_stamp`, t2.`titre`, NULL, t2.`oeuvre_id` from `partie` as t2")
        #cursor9.execute("insert into `archives_media` (`id`, `archive_id`, `comments`, `confidentiality`, `duration`, `file`, `file_ext`, `file_int`, `media`, `mime_type`, `order`, `publisher_id`, `record_type`, `summary`, `time_stamp`, `title`, `user_id`, `work_id`) select t2.`id`, t2.`volume_id`, t2.`notes`, t2.`confidentialite_partie`, t2.`duree`, t2.`audio`, t2.`audio_ext`, t2.`audio_int`,  CONCAT(t2.`volume_id`, t2.`seq`), NULL, t2.`seq`, t2.`editeur_partition_id`, NULL, NULL, t2.`time_stamp`, t2.`titre`, NULL, t2.`oeuvre_id` from `partie` as t2")

        cursor10 = connection.cursor()
        cursor10.execute("insert into `archives_archive_tags` (`archive_id`, `tag_id`) select t2.`volume_id`, t2.`tagevenement_id` from `volume_tag_evenements` as t2")

        cursor11 = connection.cursor()
        cursor11.execute("insert into `archives_archive_tags` (`archive_id`, `tag_id`) select t2.`videovolume_id`, t2.`tagevenement_id` from `video_volume_tag_evenements` as t2")

        cursor12 = connection.cursor()
        cursor12.execute("insert ignore into `archives_archive_collectivities` (`archive_id`, `collectivity_id`) select t2.`volume_id`, t2.`collectivite_id` from `volume_collectivite` as t2")

        cursor13 = connection.cursor()
        cursor13.execute("insert into `archives_archive_collectivities` (`archive_id`, `collectivity_id`) select t2.`video_volume_id`, t2.`collectivite_id` from `video_volume_collectivite` as t2")

        '''
        media_id = INT
        hack : on insere id des tables partie_collectivite et video_record_collectivite
        puis insertion en fin de migration par les bons media_id en jointure avec les tables
        '''

        cursor14 = connection.cursor()
        cursor14.execute("insert into archives_media_collectivities (media_id, collectivity_id) select t2.id, t1.collectivite_id from partie_collectivite as t1, archives_media as t2 where BINARY t1.partie_id = BINARY CONCAT(SUBSTRING(media,1,10),'-0',`order`) AND t2.media like ('AU%%') and t2.`order`<10")

        cursor15 = connection.cursor()
        cursor15.execute("insert into archives_media_collectivities (media_id, collectivity_id) select t2.id, t1.collectivite_id from partie_collectivite as t1, archives_media as t2 where BINARY t1.partie_id = BINARY CONCAT(SUBSTRING(media,1,10),'-',`order`) AND t2.media like ('AU%%') and t2.`order`>=10")

        cursor16 = connection.cursor()
        cursor16.execute("insert into `archives_media_collectivities` (`media_id`, `collectivity_id`) select t2.`video_record_id`, t2.`collectivite_id` from `video_record_collectivite` as t2")

        transaction.commit_unless_managed()

    def backwards(self, orm):
        pass

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
    symmetrical = True
