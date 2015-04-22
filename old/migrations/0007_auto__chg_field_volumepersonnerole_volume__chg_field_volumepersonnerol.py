# -*- coding: utf-8 -*-
import datetime
from south.db import db
from south.v2 import SchemaMigration
from django.db import models


class Migration(SchemaMigration):

    def forwards(self, orm):

        # Renaming column for 'VolumePersonneRole.volume' to match new field type.
        db.rename_column(u'volume_personne_role', 'volume', 'volume_id')
        # Changing field 'VolumePersonneRole.volume'
        db.alter_column(u'volume_personne_role', 'volume_id', self.gf('django.db.models.fields.related.ForeignKey')(to=orm['old.Volume']))
        # Adding index on 'VolumePersonneRole', fields ['volume']
        db.create_index(u'volume_personne_role', ['volume_id'])


        # Renaming column for 'VolumePersonneRole.personne' to match new field type.
        db.rename_column(u'volume_personne_role', 'personne', 'personne_id')
        # Changing field 'VolumePersonneRole.personne'
        db.alter_column(u'volume_personne_role', 'personne_id', self.gf('django.db.models.fields.related.ForeignKey')(to=orm['old.Personne']))
        # Adding index on 'VolumePersonneRole', fields ['personne']
        db.create_index(u'volume_personne_role', ['personne_id'])


        # Renaming column for 'VolumePersonneRole.role' to match new field type.
        db.rename_column(u'volume_personne_role', 'role', 'role_id')
        # Changing field 'VolumePersonneRole.role'
        db.alter_column(u'volume_personne_role', 'role_id', self.gf('django.db.models.fields.related.ForeignKey')(to=orm['old.Role']))
        # Adding index on 'VolumePersonneRole', fields ['role']
        db.create_index(u'volume_personne_role', ['role_id'])


    def backwards(self, orm):
        # Removing index on 'VolumePersonneRole', fields ['role']
        db.delete_index(u'volume_personne_role', ['role_id'])

        # Removing index on 'VolumePersonneRole', fields ['personne']
        db.delete_index(u'volume_personne_role', ['personne_id'])

        # Removing index on 'VolumePersonneRole', fields ['volume']
        db.delete_index(u'volume_personne_role', ['volume_id'])


        # Renaming column for 'VolumePersonneRole.volume' to match new field type.
        db.rename_column(u'volume_personne_role', 'volume_id', 'volume')
        # Changing field 'VolumePersonneRole.volume'
        db.alter_column(u'volume_personne_role', 'volume', self.gf('django.db.models.fields.CharField')(max_length=30))

        # Renaming column for 'VolumePersonneRole.personne' to match new field type.
        db.rename_column(u'volume_personne_role', 'personne_id', 'personne')
        # Changing field 'VolumePersonneRole.personne'
        db.alter_column(u'volume_personne_role', 'personne', self.gf('django.db.models.fields.IntegerField')())

        # Renaming column for 'VolumePersonneRole.role' to match new field type.
        db.rename_column(u'volume_personne_role', 'role_id', 'role')
        # Changing field 'VolumePersonneRole.role'
        db.alter_column(u'volume_personne_role', 'role', self.gf('django.db.models.fields.IntegerField')())

    models = {
        'old.collectivite': {
            'Meta': {'object_name': 'Collectivite', 'db_table': "u'collectivite'"},
            'forme_canonique': ('django.db.models.fields.IntegerField', [], {}),
            'id': ('django.db.models.fields.IntegerField', [], {'primary_key': 'True'}),
            'indice': ('django.db.models.fields.IntegerField', [], {}),
            'nom': ('django.db.models.fields.CharField', [], {'unique': 'True', 'max_length': '255'}),
            'supprime': ('django.db.models.fields.IntegerField', [], {'unique': 'True'})
        },
        'old.contrat': {
            'Meta': {'object_name': 'Contrat', 'db_table': "u'contrat'"},
            'id': ('django.db.models.fields.IntegerField', [], {'primary_key': 'True'}),
            'intitule': ('django.db.models.fields.CharField', [], {'unique': 'True', 'max_length': '255'}),
            'mime_type': ('django.db.models.fields.CharField', [], {'max_length': '765'}),
            'notes': ('django.db.models.fields.TextField', [], {}),
            'num_pages': ('django.db.models.fields.IntegerField', [], {'null': 'True', 'blank': 'True'}),
            'parent': ('django.db.models.fields.CharField', [], {'max_length': '48'}),
            'supprime': ('django.db.models.fields.IntegerField', [], {'unique': 'True'}),
            'technicien': ('django.db.models.fields.IntegerField', [], {}),
            'time_stamp': ('django.db.models.fields.DateTimeField', [], {}),
            'type': ('django.db.models.fields.IntegerField', [], {})
        },
        'old.evenement': {
            'Meta': {'object_name': 'Evenement', 'db_table': "u'evenement'"},
            'audio_children': ('django.db.models.fields.IntegerField', [], {}),
            'date_debut': ('django.db.models.fields.DateField', [], {'null': 'True', 'blank': 'True'}),
            'date_fin': ('django.db.models.fields.DateField', [], {'null': 'True', 'blank': 'True'}),
            'event_children': ('django.db.models.fields.IntegerField', [], {}),
            'id': ('django.db.models.fields.IntegerField', [], {'primary_key': 'True'}),
            'intitule': ('django.db.models.fields.CharField', [], {'unique': 'True', 'max_length': '255'}),
            'parent': ('django.db.models.fields.IntegerField', [], {}),
            'pdf_children': ('django.db.models.fields.IntegerField', [], {}),
            'sous_titre': ('django.db.models.fields.CharField', [], {'max_length': '384'}),
            'supprime': ('django.db.models.fields.IntegerField', [], {'unique': 'True'}),
            'time_stamp': ('django.db.models.fields.DateTimeField', [], {}),
            'type': ('django.db.models.fields.IntegerField', [], {}),
            'video_children': ('django.db.models.fields.IntegerField', [], {})
        },
        'old.lieu': {
            'Meta': {'object_name': 'Lieu', 'db_table': "u'lieu'"},
            'id': ('django.db.models.fields.IntegerField', [], {'primary_key': 'True'}),
            'nom': ('django.db.models.fields.CharField', [], {'unique': 'True', 'max_length': '255'}),
            'pays': ('django.db.models.fields.CharField', [], {'max_length': '765'}),
            'salle': ('django.db.models.fields.CharField', [], {'unique': 'True', 'max_length': '255'}),
            'supprime': ('django.db.models.fields.IntegerField', [], {'unique': 'True'}),
            'ville': ('django.db.models.fields.CharField', [], {'max_length': '765'})
        },
        'old.notepersonneroleedit': {
            'Meta': {'object_name': 'NotePersonneRoleEdit', 'db_table': "u'note_personne_role_edit'"},
            'id': ('django.db.models.fields.IntegerField', [], {'primary_key': 'True'}),
            'note_programme': ('django.db.models.fields.IntegerField', [], {}),
            'personne': ('django.db.models.fields.IntegerField', [], {}),
            'role': ('django.db.models.fields.IntegerField', [], {})
        },
        'old.noteprogramme': {
            'Meta': {'object_name': 'NoteProgramme', 'db_table': "u'note_programme'"},
            'confidentialite': ('django.db.models.fields.IntegerField', [], {}),
            'date_transfert': ('django.db.models.fields.DateField', [], {'null': 'True', 'blank': 'True'}),
            'editeur': ('django.db.models.fields.IntegerField', [], {}),
            'etat_note': ('django.db.models.fields.IntegerField', [], {}),
            'id': ('django.db.models.fields.IntegerField', [], {'primary_key': 'True'}),
            'id_loris': ('django.db.models.fields.CharField', [], {'unique': 'True', 'max_length': '15'}),
            'intitule': ('django.db.models.fields.CharField', [], {'unique': 'True', 'max_length': '255'}),
            'mime_type': ('django.db.models.fields.CharField', [], {'max_length': '765'}),
            'notes': ('django.db.models.fields.TextField', [], {}),
            'num_pages': ('django.db.models.fields.IntegerField', [], {'null': 'True', 'blank': 'True'}),
            'parent': ('django.db.models.fields.IntegerField', [], {}),
            'supprime': ('django.db.models.fields.IntegerField', [], {'unique': 'True'}),
            'technicien': ('django.db.models.fields.IntegerField', [], {}),
            'time_stamp': ('django.db.models.fields.DateTimeField', [], {}),
            'type': ('django.db.models.fields.IntegerField', [], {})
        },
        'old.oeuvre': {
            'Meta': {'object_name': 'Oeuvre', 'db_table': "u'oeuvre'"},
            'annee': ('django.db.models.fields.CharField', [], {'unique': 'True', 'max_length': '12'}),
            'id': ('django.db.models.fields.IntegerField', [], {'primary_key': 'True'}),
            'sous_titre': ('django.db.models.fields.CharField', [], {'max_length': '384'}),
            'supprime': ('django.db.models.fields.IntegerField', [], {'unique': 'True'}),
            'titre': ('django.db.models.fields.CharField', [], {'max_length': '384'})
        },
        'old.oeuvrepersonnerole': {
            'Meta': {'object_name': 'OeuvrePersonneRole', 'db_table': "u'oeuvre_personne_role'"},
            'id': ('django.db.models.fields.IntegerField', [], {'primary_key': 'True'}),
            'oeuvre': ('django.db.models.fields.IntegerField', [], {}),
            'personne': ('django.db.models.fields.IntegerField', [], {}),
            'role': ('django.db.models.fields.IntegerField', [], {})
        },
        'old.partie': {
            'Meta': {'ordering': "['seq']", 'object_name': 'Partie', 'db_table': "u'partie'"},
            'auteur1': ('django.db.models.fields.IntegerField', [], {'null': 'True', 'blank': 'True'}),
            'auteur2': ('django.db.models.fields.IntegerField', [], {'null': 'True', 'blank': 'True'}),
            'auteur3': ('django.db.models.fields.IntegerField', [], {'null': 'True', 'blank': 'True'}),
            'auteur4': ('django.db.models.fields.IntegerField', [], {'null': 'True', 'blank': 'True'}),
            'brahms_key': ('django.db.models.fields.CharField', [], {'max_length': '27'}),
            'confidentialite_partie': ('django.db.models.fields.IntegerField', [], {}),
            'doris_key': ('django.db.models.fields.IntegerField', [], {}),
            'duree': ('django.db.models.fields.TextField', [], {'blank': 'True'}),
            'editeur_partition': ('django.db.models.fields.IntegerField', [], {}),
            'id': ('django.db.models.fields.CharField', [], {'max_length': '36', 'primary_key': 'True'}),
            'notes': ('django.db.models.fields.CharField', [], {'max_length': '765'}),
            'oeuvre': ('django.db.models.fields.related.ForeignKey', [], {'to': "orm['old.Oeuvre']"}),
            'partype': ('django.db.models.fields.IntegerField', [], {}),
            'resume': ('django.db.models.fields.TextField', [], {}),
            'resume_na': ('django.db.models.fields.TextField', [], {}),
            'seq': ('django.db.models.fields.IntegerField', [], {}),
            'supprime': ('django.db.models.fields.IntegerField', [], {}),
            'time_stamp': ('django.db.models.fields.DateTimeField', [], {}),
            'titre': ('django.db.models.fields.TextField', [], {}),
            'titre_na': ('django.db.models.fields.TextField', [], {}),
            'volume': ('django.db.models.fields.related.ForeignKey', [], {'to': "orm['old.Volume']", 'null': 'True', 'blank': 'True'})
        },
        'old.partiecollectivite': {
            'Meta': {'object_name': 'PartieCollectivite', 'db_table': "u'partie_collectivite'"},
            'collectivite': ('django.db.models.fields.IntegerField', [], {}),
            'id': ('django.db.models.fields.IntegerField', [], {'primary_key': 'True'}),
            'partie': ('django.db.models.fields.CharField', [], {'max_length': '45'})
        },
        'old.partiepersonnerole': {
            'Meta': {'object_name': 'PartiePersonneRole', 'db_table': "u'partie_personne_role'"},
            'id': ('django.db.models.fields.IntegerField', [], {'primary_key': 'True'}),
            'partie': ('django.db.models.fields.CharField', [], {'max_length': '45'}),
            'personne': ('django.db.models.fields.IntegerField', [], {}),
            'role': ('django.db.models.fields.IntegerField', [], {})
        },
        'old.personne': {
            'Meta': {'object_name': 'Personne', 'db_table': "u'personne'"},
            'brahms_key': ('django.db.models.fields.CharField', [], {'max_length': '27'}),
            'doris_key': ('django.db.models.fields.IntegerField', [], {}),
            'fonction': ('django.db.models.fields.CharField', [], {'max_length': '90'}),
            'forme_canonique': ('django.db.models.fields.IntegerField', [], {}),
            'id': ('django.db.models.fields.IntegerField', [], {'primary_key': 'True'}),
            'indice': ('django.db.models.fields.IntegerField', [], {}),
            'nom': ('django.db.models.fields.CharField', [], {'max_length': '150'}),
            'nom_na': ('django.db.models.fields.CharField', [], {'max_length': '150'}),
            'prenom': ('django.db.models.fields.CharField', [], {'max_length': '150'}),
            'prenom_na': ('django.db.models.fields.CharField', [], {'max_length': '150'}),
            'supprime': ('django.db.models.fields.IntegerField', [], {})
        },
        'old.precalc': {
            'Meta': {'object_name': 'Precalc', 'db_table': "u'precalc'"},
            'auto_id': ('django.db.models.fields.IntegerField', [], {'primary_key': 'True'}),
            'creation_stamp': ('django.db.models.fields.DateTimeField', [], {}),
            'dc_data': ('django.db.models.fields.TextField', [], {}),
            'mods_data': ('django.db.models.fields.TextField', [], {}),
            'oai_id': ('django.db.models.fields.CharField', [], {'max_length': '96'}),
            'orig_id': ('django.db.models.fields.CharField', [], {'max_length': '48'}),
            'supprime': ('django.db.models.fields.IntegerField', [], {}),
            'type': ('django.db.models.fields.CharField', [], {'max_length': '48'})
        },
        'old.role': {
            'Meta': {'object_name': 'Role', 'db_table': "u'role'"},
            'forme_canonique': ('django.db.models.fields.IntegerField', [], {}),
            'id': ('django.db.models.fields.IntegerField', [], {'primary_key': 'True'}),
            'indice': ('django.db.models.fields.IntegerField', [], {}),
            'intitule': ('django.db.models.fields.CharField', [], {'unique': 'True', 'max_length': '255'}),
            'supprime': ('django.db.models.fields.IntegerField', [], {'unique': 'True'})
        },
        'old.roleedit': {
            'Meta': {'object_name': 'RoleEdit', 'db_table': "u'role_edit'"},
            'forme_canonique': ('django.db.models.fields.IntegerField', [], {}),
            'id': ('django.db.models.fields.IntegerField', [], {'primary_key': 'True'}),
            'indice': ('django.db.models.fields.IntegerField', [], {}),
            'intitule': ('django.db.models.fields.CharField', [], {'unique': 'True', 'max_length': '255'}),
            'supprime': ('django.db.models.fields.IntegerField', [], {'unique': 'True'})
        },
        'old.testviewoairecords': {
            'Meta': {'object_name': 'TestViewOaiRecords', 'db_table': "u'test_view_oai_records'"},
            'confidentialite': ('django.db.models.fields.CharField', [], {'max_length': '33'}),
            'date_debut': ('django.db.models.fields.CharField', [], {'max_length': '30', 'blank': 'True'}),
            'date_fin': ('django.db.models.fields.CharField', [], {'max_length': '30', 'blank': 'True'}),
            'date_pub': ('django.db.models.fields.CharField', [], {'max_length': '30', 'blank': 'True'}),
            'debut_parent': ('django.db.models.fields.DateField', [], {'null': 'True', 'blank': 'True'}),
            'fin_parent': ('django.db.models.fields.DateField', [], {'null': 'True', 'blank': 'True'}),
            'id': ('django.db.models.fields.CharField', [], {'max_length': '48', 'primary_key': 'True'}),
            'id_loris': ('django.db.models.fields.CharField', [], {'max_length': '15'}),
            'oai_set': ('django.db.models.fields.CharField', [], {'max_length': '21'}),
            'parent': ('django.db.models.fields.IntegerField', [], {}),
            'place': ('django.db.models.fields.CharField', [], {'max_length': '384'}),
            'publisher': ('django.db.models.fields.CharField', [], {'max_length': '765'}),
            'sous_titre': ('django.db.models.fields.CharField', [], {'max_length': '384'}),
            'supprime': ('django.db.models.fields.IntegerField', [], {}),
            'time_stamp': ('django.db.models.fields.DateTimeField', [], {}),
            'titre': ('django.db.models.fields.CharField', [], {'max_length': '765', 'blank': 'True'}),
            'titre_parent': ('django.db.models.fields.CharField', [], {'max_length': '765', 'blank': 'True'}),
            'type_event': ('django.db.models.fields.CharField', [], {'max_length': '12', 'blank': 'True'}),
            'type_notice': ('django.db.models.fields.BigIntegerField', [], {})
        },
        'old.typeevenement': {
            'Meta': {'object_name': 'TypeEvenement', 'db_table': "u'type_evenement'"},
            'id': ('django.db.models.fields.IntegerField', [], {'primary_key': 'True'}),
            'intitule': ('django.db.models.fields.CharField', [], {'unique': 'True', 'max_length': '255'}),
            'supprime': ('django.db.models.fields.IntegerField', [], {'unique': 'True'})
        },
        'old.utilisateur': {
            'Meta': {'object_name': 'Utilisateur', 'db_table': "u'utilisateur'"},
            'alt_login': ('django.db.models.fields.CharField', [], {'max_length': '384'}),
            'droits': ('django.db.models.fields.IntegerField', [], {}),
            'id': ('django.db.models.fields.IntegerField', [], {'primary_key': 'True'}),
            'nom': ('django.db.models.fields.CharField', [], {'unique': 'True', 'max_length': '255'}),
            'prenom': ('django.db.models.fields.CharField', [], {'unique': 'True', 'max_length': '255'}),
            'supprime': ('django.db.models.fields.IntegerField', [], {})
        },
        'old.videorecord': {
            'Meta': {'object_name': 'VideoRecord', 'db_table': "u'video_record'"},
            'archived': ('django.db.models.fields.IntegerField', [], {}),
            'archived_file_name': ('django.db.models.fields.CharField', [], {'max_length': '192'}),
            'confidentialite_record': ('django.db.models.fields.IntegerField', [], {}),
            'date_transfert': ('django.db.models.fields.DateField', [], {'null': 'True', 'blank': 'True'}),
            'duree': ('django.db.models.fields.TextField', [], {}),
            'id': ('django.db.models.fields.IntegerField', [], {'primary_key': 'True'}),
            'intitule': ('django.db.models.fields.TextField', [], {}),
            'mime_type': ('django.db.models.fields.CharField', [], {'max_length': '192'}),
            'new_x': ('django.db.models.fields.IntegerField', [], {}),
            'new_y': ('django.db.models.fields.IntegerField', [], {}),
            'notes': ('django.db.models.fields.TextField', [], {'blank': 'True'}),
            'old_x': ('django.db.models.fields.IntegerField', [], {}),
            'old_y': ('django.db.models.fields.IntegerField', [], {}),
            'online': ('django.db.models.fields.IntegerField', [], {}),
            'parent': ('django.db.models.fields.CharField', [], {'max_length': '48'}),
            'resume': ('django.db.models.fields.TextField', [], {}),
            'supprime': ('django.db.models.fields.IntegerField', [], {}),
            'technicien': ('django.db.models.fields.IntegerField', [], {}),
            'temp_file_name': ('django.db.models.fields.CharField', [], {'max_length': '384'}),
            'time_stamp': ('django.db.models.fields.DateTimeField', [], {}),
            'type': ('django.db.models.fields.IntegerField', [], {'null': 'True', 'blank': 'True'}),
            'type_record': ('django.db.models.fields.IntegerField', [], {})
        },
        'old.videorecordcollectivite': {
            'Meta': {'object_name': 'VideoRecordCollectivite', 'db_table': "u'video_record_collectivite'"},
            'collectivite': ('django.db.models.fields.IntegerField', [], {}),
            'id': ('django.db.models.fields.IntegerField', [], {'primary_key': 'True'}),
            'video_record': ('django.db.models.fields.CharField', [], {'max_length': '30'})
        },
        'old.videorecordpersonnerole': {
            'Meta': {'object_name': 'VideoRecordPersonneRole', 'db_table': "u'video_record_personne_role'"},
            'id': ('django.db.models.fields.IntegerField', [], {'primary_key': 'True'}),
            'personne': ('django.db.models.fields.IntegerField', [], {}),
            'role': ('django.db.models.fields.IntegerField', [], {}),
            'video_record': ('django.db.models.fields.CharField', [], {'max_length': '30'})
        },
        'old.videoset': {
            'Meta': {'object_name': 'VideoSet', 'db_table': "u'video_set'"},
            'date_debut': ('django.db.models.fields.DateField', [], {'null': 'True', 'blank': 'True'}),
            'date_fin': ('django.db.models.fields.DateField', [], {'null': 'True', 'blank': 'True'}),
            'id': ('django.db.models.fields.IntegerField', [], {'primary_key': 'True'}),
            'intitule': ('django.db.models.fields.CharField', [], {'unique': 'True', 'max_length': '255'}),
            'notes': ('django.db.models.fields.TextField', [], {}),
            'parent': ('django.db.models.fields.IntegerField', [], {}),
            'resume': ('django.db.models.fields.TextField', [], {}),
            'sous_titre': ('django.db.models.fields.CharField', [], {'max_length': '384'}),
            'supprime': ('django.db.models.fields.IntegerField', [], {'unique': 'True'}),
            'time_stamp': ('django.db.models.fields.DateTimeField', [], {})
        },
        'old.videovolume': {
            'Meta': {'object_name': 'VideoVolume', 'db_table': "u'video_volume'"},
            'annee': ('django.db.models.fields.TextField', [], {'blank': 'True'}),
            'date': ('django.db.models.fields.DateField', [], {'null': 'True', 'blank': 'True'}),
            'date_transfert': ('django.db.models.fields.DateField', [], {'null': 'True', 'blank': 'True'}),
            'horaire': ('django.db.models.fields.CharField', [], {'max_length': '15'}),
            'id': ('django.db.models.fields.CharField', [], {'max_length': '36', 'primary_key': 'True'}),
            'intitule': ('django.db.models.fields.TextField', [], {}),
            'lieu': ('django.db.models.fields.IntegerField', [], {}),
            'notes': ('django.db.models.fields.TextField', [], {'blank': 'True'}),
            'parent': ('django.db.models.fields.IntegerField', [], {}),
            'resume': ('django.db.models.fields.TextField', [], {}),
            'sort': ('django.db.models.fields.CharField', [], {'max_length': '6'}),
            'supprime': ('django.db.models.fields.IntegerField', [], {}),
            'technicien': ('django.db.models.fields.IntegerField', [], {}),
            'time_stamp': ('django.db.models.fields.DateTimeField', [], {}),
            'type': ('django.db.models.fields.IntegerField', [], {'null': 'True', 'blank': 'True'})
        },
        'old.videovolumecollectivite': {
            'Meta': {'object_name': 'VideoVolumeCollectivite', 'db_table': "u'video_volume_collectivite'"},
            'collectivite': ('django.db.models.fields.IntegerField', [], {}),
            'id': ('django.db.models.fields.IntegerField', [], {'primary_key': 'True'}),
            'video_volume': ('django.db.models.fields.CharField', [], {'max_length': '30'})
        },
        'old.videovolumepersonnerole': {
            'Meta': {'object_name': 'VideoVolumePersonneRole', 'db_table': "u'video_volume_personne_role'"},
            'id': ('django.db.models.fields.IntegerField', [], {'primary_key': 'True'}),
            'personne': ('django.db.models.fields.IntegerField', [], {}),
            'role': ('django.db.models.fields.IntegerField', [], {}),
            'video_volume': ('django.db.models.fields.CharField', [], {'max_length': '30'})
        },
        'old.viewcomposrussesoeuvres': {
            'Meta': {'object_name': 'ViewComposRussesOeuvres', 'db_table': "u'_view_compos_russes_oeuvres'"},
            'compositeur': ('django.db.models.fields.CharField', [], {'max_length': '306'}),
            'date_debut': ('django.db.models.fields.DateField', [], {'null': 'True', 'blank': 'True'}),
            'date_fin': ('django.db.models.fields.DateField', [], {'null': 'True', 'blank': 'True'}),
            'id': ('django.db.models.fields.CharField', [], {'max_length': '36', 'primary_key': 'True'}),
            'oeuvre_sous_titre': ('django.db.models.fields.CharField', [], {'max_length': '384'}),
            'oeuvre_titre': ('django.db.models.fields.CharField', [], {'max_length': '384'}),
            'titre_concat': ('django.db.models.fields.CharField', [], {'max_length': '384', 'blank': 'True'})
        },
        'old.viewevenementvolume': {
            'Meta': {'object_name': 'ViewEvenementVolume', 'db_table': "u'_view_evenement_volume'"},
            'titre_concat': ('django.db.models.fields.CharField', [], {'max_length': '384', 'blank': 'True'}),
            'titre_simple': ('django.db.models.fields.CharField', [], {'max_length': '765', 'blank': 'True'}),
            'volume_id': ('django.db.models.fields.CharField', [], {'max_length': '36', 'primary_key': 'True'})
        },
        'old.viewtitreoeuvrepersonnerole': {
            'Meta': {'object_name': 'ViewTitreOeuvrePersonneRole', 'db_table': "u'view_titre_oeuvre_personne_role'"},
            'auteur_personne_id': ('django.db.models.fields.IntegerField', [], {'null': 'True', 'blank': 'True'}),
            'collectivite_id': ('django.db.models.fields.IntegerField', [], {'null': 'True', 'blank': 'True'}),
            'intervenant_personne_id': ('django.db.models.fields.CharField', [], {'max_length': '16', 'blank': 'True'}),
            'intervenant_role_id': ('django.db.models.fields.CharField', [], {'max_length': '16', 'blank': 'True'}),
            'partie_id': ('django.db.models.fields.CharField', [], {'max_length': '36', 'primary_key': 'True'}),
            'titre': ('django.db.models.fields.CharField', [], {'max_length': '96', 'blank': 'True'})
        },
        'old.volume': {
            'Meta': {'object_name': 'Volume', 'db_table': "u'volume'"},
            'annee': ('django.db.models.fields.TextField', [], {'blank': 'True'}),
            'auteur': ('django.db.models.fields.TextField', [], {'blank': 'True'}),
            'cddb': ('django.db.models.fields.CharField', [], {'max_length': '24', 'db_column': "'CDDB'", 'blank': 'True'}),
            'confidentialite_volume': ('django.db.models.fields.IntegerField', [], {}),
            'date': ('django.db.models.fields.DateField', [], {'null': 'True', 'blank': 'True'}),
            'date_transfert': ('django.db.models.fields.DateField', [], {'null': 'True', 'blank': 'True'}),
            'doris_key': ('django.db.models.fields.IntegerField', [], {}),
            'etat_archive': ('django.db.models.fields.IntegerField', [], {}),
            'etat_collection': ('django.db.models.fields.IntegerField', [], {}),
            'horaire': ('django.db.models.fields.CharField', [], {'max_length': '15'}),
            'id': ('django.db.models.fields.CharField', [], {'max_length': '36', 'primary_key': 'True'}),
            'intitule': ('django.db.models.fields.TextField', [], {}),
            'intitule_na': ('django.db.models.fields.TextField', [], {}),
            'label': ('django.db.models.fields.TextField', [], {'blank': 'True'}),
            'lieu': ('django.db.models.fields.IntegerField', [], {}),
            'note2prog_id': ('django.db.models.fields.CharField', [], {'max_length': '30'}),
            'notes': ('django.db.models.fields.TextField', [], {'blank': 'True'}),
            'notes_na': ('django.db.models.fields.TextField', [], {'blank': 'True'}),
            'old_id': ('django.db.models.fields.CharField', [], {'max_length': '384'}),
            'parent': ('django.db.models.fields.related.ForeignKey', [], {'to': "orm['old.Evenement']"}),
            'pending': ('django.db.models.fields.IntegerField', [], {}),
            'pret': ('django.db.models.fields.IntegerField', [], {}),
            'resume': ('django.db.models.fields.TextField', [], {}),
            'supprime': ('django.db.models.fields.IntegerField', [], {}),
            'technicien': ('django.db.models.fields.related.ForeignKey', [], {'to': "orm['old.Utilisateur']"}),
            'time_stamp': ('django.db.models.fields.DateTimeField', [], {}),
            'url': ('django.db.models.fields.TextField', [], {'blank': 'True'}),
            'voltype': ('django.db.models.fields.IntegerField', [], {})
        },
        'old.volumecollectivite': {
            'Meta': {'object_name': 'VolumeCollectivite', 'db_table': "u'volume_collectivite'"},
            'collectivite': ('django.db.models.fields.related.ForeignKey', [], {'to': "orm['old.Collectivite']"}),
            'id': ('django.db.models.fields.IntegerField', [], {'primary_key': 'True'}),
            'volume': ('django.db.models.fields.related.ForeignKey', [], {'to': "orm['old.Volume']"})
        },
        'old.volumepersonnerole': {
            'Meta': {'object_name': 'VolumePersonneRole', 'db_table': "u'volume_personne_role'"},
            'id': ('django.db.models.fields.IntegerField', [], {'primary_key': 'True'}),
            'personne': ('django.db.models.fields.related.ForeignKey', [], {'to': "orm['old.Personne']"}),
            'role': ('django.db.models.fields.related.ForeignKey', [], {'to': "orm['old.Role']"}),
            'volume': ('django.db.models.fields.related.ForeignKey', [], {'to': "orm['old.Volume']"})
        }
    }

    complete_apps = ['old']