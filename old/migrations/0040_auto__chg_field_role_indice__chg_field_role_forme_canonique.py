# -*- coding: utf-8 -*-
import datetime
from south.db import db
from south.v2 import SchemaMigration
from django.db import models


class Migration(SchemaMigration):

    def forwards(self, orm):

        # Changing field 'Role.indice'
        db.alter_column(u'role', 'indice', self.gf('django.db.models.fields.IntegerField')(null=True))

        # Changing field 'Role.forme_canonique'
        db.alter_column(u'role', 'forme_canonique_id', self.gf('django.db.models.fields.related.ForeignKey')(to=orm['old.Role'], null=True))

    def backwards(self, orm):

        # User chose to not deal with backwards NULL issues for 'Role.indice'
        raise RuntimeError("Cannot reverse this migration. 'Role.indice' and its values cannot be restored.")

        # User chose to not deal with backwards NULL issues for 'Role.forme_canonique'
        raise RuntimeError("Cannot reverse this migration. 'Role.forme_canonique' and its values cannot be restored.")

    models = {
        'old.collectivite': {
            'Meta': {'object_name': 'Collectivite', 'db_table': "u'collectivite'"},
            'forme_canonique': ('django.db.models.fields.IntegerField', [], {}),
            'id': ('django.db.models.fields.IntegerField', [], {'primary_key': 'True'}),
            'indice': ('django.db.models.fields.IntegerField', [], {}),
            'nom': ('django.db.models.fields.CharField', [], {'unique': 'True', 'max_length': '255'}),
            'supprime': ('django.db.models.fields.IntegerField', [], {})
        },
        'old.contrat': {
            'Meta': {'object_name': 'Contrat', 'db_table': "u'contrat'"},
            'contract': ('django.db.models.fields.files.FileField', [], {'max_length': '100', 'null': 'True', 'blank': 'True'}),
            'id': ('django.db.models.fields.IntegerField', [], {'primary_key': 'True'}),
            'intitule': ('django.db.models.fields.CharField', [], {'max_length': '255'}),
            'mime_type': ('django.db.models.fields.CharField', [], {'max_length': '765'}),
            'notes': ('django.db.models.fields.TextField', [], {}),
            'num_pages': ('django.db.models.fields.IntegerField', [], {'null': 'True', 'blank': 'True'}),
            'parent': ('django.db.models.fields.related.ForeignKey', [], {'to': "orm['old.VideoVolume']"}),
            'supprime': ('django.db.models.fields.IntegerField', [], {}),
            'technicien': ('django.db.models.fields.related.ForeignKey', [], {'to': "orm['old.Utilisateur']"}),
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
            'parent': ('django.db.models.fields.related.ForeignKey', [], {'to': "orm['old.Evenement']"}),
            'pdf_children': ('django.db.models.fields.IntegerField', [], {}),
            'sous_titre': ('django.db.models.fields.CharField', [], {'max_length': '384'}),
            'supprime': ('django.db.models.fields.IntegerField', [], {}),
            'time_stamp': ('django.db.models.fields.DateTimeField', [], {}),
            'type': ('django.db.models.fields.IntegerField', [], {}),
            'video_children': ('django.db.models.fields.IntegerField', [], {})
        },
        'old.lieu': {
            'Meta': {'object_name': 'Lieu', 'db_table': "u'lieu'"},
            'id': ('django.db.models.fields.IntegerField', [], {'primary_key': 'True'}),
            'nom': ('django.db.models.fields.CharField', [], {'unique': 'True', 'max_length': '255'}),
            'pays': ('django.db.models.fields.CharField', [], {'max_length': '765'}),
            'salle': ('django.db.models.fields.CharField', [], {'max_length': '255'}),
            'supprime': ('django.db.models.fields.IntegerField', [], {}),
            'ville': ('django.db.models.fields.CharField', [], {'max_length': '765'})
        },
        'old.notepersonneroleedit': {
            'Meta': {'object_name': 'NotePersonneRoleEdit', 'db_table': "u'note_personne_role_edit'"},
            'id': ('django.db.models.fields.IntegerField', [], {'primary_key': 'True'}),
            'note_programme': ('django.db.models.fields.IntegerField', [], {}),
            'personne': ('django.db.models.fields.related.ForeignKey', [], {'to': "orm['old.Personne']"}),
            'role': ('django.db.models.fields.related.ForeignKey', [], {'to': "orm['old.Role']"})
        },
        'old.noteprogramme': {
            'Meta': {'object_name': 'NoteProgramme', 'db_table': "u'note_programme'"},
            'confidentialite': ('django.db.models.fields.IntegerField', [], {}),
            'date_transfert': ('django.db.models.fields.DateField', [], {'null': 'True', 'blank': 'True'}),
            'editeur': ('django.db.models.fields.related.ForeignKey', [], {'to': "orm['old.Collectivite']"}),
            'etat_note': ('django.db.models.fields.IntegerField', [], {}),
            'id': ('django.db.models.fields.IntegerField', [], {'primary_key': 'True'}),
            'id_loris': ('django.db.models.fields.CharField', [], {'unique': 'True', 'max_length': '15'}),
            'intitule': ('django.db.models.fields.CharField', [], {'max_length': '255'}),
            'mime_type': ('django.db.models.fields.CharField', [], {'max_length': '765'}),
            'notes': ('django.db.models.fields.TextField', [], {}),
            'num_pages': ('django.db.models.fields.IntegerField', [], {'null': 'True', 'blank': 'True'}),
            'parent': ('django.db.models.fields.related.ForeignKey', [], {'to': "orm['old.Evenement']"}),
            'program': ('django.db.models.fields.files.FileField', [], {'max_length': '100', 'null': 'True', 'blank': 'True'}),
            'program_ext': ('django.db.models.fields.files.FileField', [], {'max_length': '100', 'null': 'True', 'blank': 'True'}),
            'program_int': ('django.db.models.fields.files.FileField', [], {'max_length': '100', 'null': 'True', 'blank': 'True'}),
            'supprime': ('django.db.models.fields.IntegerField', [], {}),
            'technicien': ('django.db.models.fields.related.ForeignKey', [], {'to': "orm['old.Utilisateur']"}),
            'time_stamp': ('django.db.models.fields.DateTimeField', [], {}),
            'type': ('django.db.models.fields.IntegerField', [], {})
        },
        'old.oeuvre': {
            'Meta': {'object_name': 'Oeuvre', 'db_table': "u'oeuvre'"},
            'annee': ('django.db.models.fields.CharField', [], {'max_length': '12'}),
            'id': ('django.db.models.fields.IntegerField', [], {'primary_key': 'True'}),
            'sous_titre': ('django.db.models.fields.CharField', [], {'max_length': '384'}),
            'supprime': ('django.db.models.fields.IntegerField', [], {}),
            'titre': ('django.db.models.fields.CharField', [], {'max_length': '384'})
        },
        'old.oeuvrepersonnerole': {
            'Meta': {'object_name': 'OeuvrePersonneRole', 'db_table': "u'oeuvre_personne_role'"},
            'id': ('django.db.models.fields.IntegerField', [], {'primary_key': 'True'}),
            'oeuvre': ('django.db.models.fields.related.ForeignKey', [], {'to': "orm['old.Oeuvre']"}),
            'personne': ('django.db.models.fields.related.ForeignKey', [], {'to': "orm['old.Personne']"}),
            'role': ('django.db.models.fields.related.ForeignKey', [], {'to': "orm['old.Role']"})
        },
        'old.partie': {
            'Meta': {'ordering': "['seq']", 'object_name': 'Partie', 'db_table': "u'partie'"},
            'audio': ('django.db.models.fields.files.FileField', [], {'max_length': '100', 'null': 'True', 'blank': 'True'}),
            'audio_ext': ('django.db.models.fields.files.FileField', [], {'max_length': '100', 'null': 'True', 'blank': 'True'}),
            'audio_int': ('django.db.models.fields.files.FileField', [], {'max_length': '100', 'null': 'True', 'blank': 'True'}),
            'auteur1': ('django.db.models.fields.IntegerField', [], {'null': 'True', 'blank': 'True'}),
            'auteur2': ('django.db.models.fields.IntegerField', [], {'null': 'True', 'blank': 'True'}),
            'auteur3': ('django.db.models.fields.IntegerField', [], {'null': 'True', 'blank': 'True'}),
            'auteur4': ('django.db.models.fields.IntegerField', [], {'null': 'True', 'blank': 'True'}),
            'brahms_key': ('django.db.models.fields.CharField', [], {'max_length': '27'}),
            'confidentialite_partie': ('django.db.models.fields.IntegerField', [], {}),
            'doris_key': ('django.db.models.fields.IntegerField', [], {}),
            'duree': ('django.db.models.fields.TextField', [], {'blank': 'True'}),
            'editeur_partition': ('django.db.models.fields.related.ForeignKey', [], {'to': "orm['old.Collectivite']"}),
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
            'collectivite': ('django.db.models.fields.related.ForeignKey', [], {'to': "orm['old.Collectivite']"}),
            'id': ('django.db.models.fields.IntegerField', [], {'primary_key': 'True'}),
            'partie': ('django.db.models.fields.related.ForeignKey', [], {'to': "orm['old.Partie']"})
        },
        'old.partiepersonnerole': {
            'Meta': {'object_name': 'PartiePersonneRole', 'db_table': "u'partie_personne_role'"},
            'id': ('django.db.models.fields.IntegerField', [], {'primary_key': 'True'}),
            'partie': ('django.db.models.fields.related.ForeignKey', [], {'to': "orm['old.Partie']"}),
            'personne': ('django.db.models.fields.related.ForeignKey', [], {'to': "orm['old.Personne']"}),
            'role': ('django.db.models.fields.related.ForeignKey', [], {'to': "orm['old.Role']"})
        },
        'old.personne': {
            'Meta': {'object_name': 'Personne', 'db_table': "u'personne'"},
            'brahms_key': ('django.db.models.fields.CharField', [], {'max_length': '27', 'null': 'True', 'blank': 'True'}),
            'doris_key': ('django.db.models.fields.IntegerField', [], {'null': 'True', 'blank': 'True'}),
            'fonction': ('django.db.models.fields.CharField', [], {'max_length': '90'}),
            'forme_canonique': ('django.db.models.fields.related.ForeignKey', [], {'to': "orm['old.Personne']", 'null': 'True', 'blank': 'True'}),
            'id': ('django.db.models.fields.IntegerField', [], {'primary_key': 'True'}),
            'indice': ('django.db.models.fields.IntegerField', [], {'null': 'True', 'blank': 'True'}),
            'nom': ('django.db.models.fields.CharField', [], {'max_length': '150'}),
            'nom_na': ('django.db.models.fields.CharField', [], {'max_length': '150', 'null': 'True', 'blank': 'True'}),
            'prenom': ('django.db.models.fields.CharField', [], {'max_length': '150'}),
            'prenom_na': ('django.db.models.fields.CharField', [], {'max_length': '150', 'null': 'True', 'blank': 'True'}),
            'supprime': ('django.db.models.fields.IntegerField', [], {})
        },
        'old.role': {
            'Meta': {'object_name': 'Role', 'db_table': "u'role'"},
            'forme_canonique': ('django.db.models.fields.related.ForeignKey', [], {'to': "orm['old.Role']", 'null': 'True', 'blank': 'True'}),
            'id': ('django.db.models.fields.IntegerField', [], {'primary_key': 'True'}),
            'indice': ('django.db.models.fields.IntegerField', [], {'null': 'True', 'blank': 'True'}),
            'intitule': ('django.db.models.fields.CharField', [], {'unique': 'True', 'max_length': '255'}),
            'supprime': ('django.db.models.fields.IntegerField', [], {'default': '0'})
        },
        'old.roleedit': {
            'Meta': {'object_name': 'RoleEdit', 'db_table': "u'role_edit'"},
            'forme_canonique': ('django.db.models.fields.related.ForeignKey', [], {'to': "orm['old.RoleEdit']"}),
            'id': ('django.db.models.fields.IntegerField', [], {'primary_key': 'True'}),
            'indice': ('django.db.models.fields.IntegerField', [], {}),
            'intitule': ('django.db.models.fields.CharField', [], {'unique': 'True', 'max_length': '255'}),
            'supprime': ('django.db.models.fields.IntegerField', [], {})
        },
        'old.typeevenement': {
            'Meta': {'object_name': 'TypeEvenement', 'db_table': "u'type_evenement'"},
            'id': ('django.db.models.fields.IntegerField', [], {'primary_key': 'True'}),
            'intitule': ('django.db.models.fields.CharField', [], {'unique': 'True', 'max_length': '255'}),
            'supprime': ('django.db.models.fields.IntegerField', [], {})
        },
        'old.utilisateur': {
            'Meta': {'object_name': 'Utilisateur', 'db_table': "u'utilisateur'"},
            'alt_login': ('django.db.models.fields.CharField', [], {'max_length': '384', 'null': 'True', 'blank': 'True'}),
            'droits': ('django.db.models.fields.IntegerField', [], {}),
            'id': ('django.db.models.fields.IntegerField', [], {'primary_key': 'True'}),
            'nom': ('django.db.models.fields.CharField', [], {'max_length': '255'}),
            'prenom': ('django.db.models.fields.CharField', [], {'max_length': '255'}),
            'supprime': ('django.db.models.fields.IntegerField', [], {'default': '0'})
        },
        'old.videorecord': {
            'Meta': {'object_name': 'VideoRecord', 'db_table': "u'video_record'"},
            'archived': ('django.db.models.fields.IntegerField', [], {'null': 'True', 'blank': 'True'}),
            'archived_file_name': ('django.db.models.fields.CharField', [], {'max_length': '192', 'null': 'True', 'blank': 'True'}),
            'confidentialite_record': ('django.db.models.fields.CharField', [], {'max_length': '1'}),
            'duree': ('django.db.models.fields.TextField', [], {}),
            'id': ('django.db.models.fields.IntegerField', [], {'primary_key': 'True'}),
            'intitule': ('django.db.models.fields.TextField', [], {}),
            'mime_type': ('django.db.models.fields.CharField', [], {'max_length': '192'}),
            'new_x': ('django.db.models.fields.IntegerField', [], {'null': 'True', 'blank': 'True'}),
            'new_y': ('django.db.models.fields.IntegerField', [], {'null': 'True', 'blank': 'True'}),
            'notes': ('django.db.models.fields.TextField', [], {'null': 'True', 'blank': 'True'}),
            'old_x': ('django.db.models.fields.IntegerField', [], {'null': 'True', 'blank': 'True'}),
            'old_y': ('django.db.models.fields.IntegerField', [], {'null': 'True', 'blank': 'True'}),
            'online': ('django.db.models.fields.IntegerField', [], {'null': 'True', 'blank': 'True'}),
            'parent': ('django.db.models.fields.related.ForeignKey', [], {'to': "orm['old.VideoVolume']"}),
            'resume': ('django.db.models.fields.TextField', [], {'null': 'True', 'blank': 'True'}),
            'supprime': ('django.db.models.fields.IntegerField', [], {'default': '0'}),
            'technicien': ('django.db.models.fields.related.ForeignKey', [], {'to': "orm['old.Utilisateur']"}),
            'temp_file_name': ('django.db.models.fields.CharField', [], {'max_length': '384', 'null': 'True', 'blank': 'True'}),
            'time_stamp': ('django.db.models.fields.DateTimeField', [], {'auto_now': 'True', 'blank': 'True'}),
            'type': ('django.db.models.fields.IntegerField', [], {'null': 'True', 'blank': 'True'}),
            'type_record': ('django.db.models.fields.CharField', [], {'max_length': '1'}),
            'video': ('django.db.models.fields.files.FileField', [], {'max_length': '100', 'null': 'True', 'blank': 'True'}),
            'video_ext': ('django.db.models.fields.files.FileField', [], {'max_length': '100', 'null': 'True', 'blank': 'True'}),
            'video_int': ('django.db.models.fields.files.FileField', [], {'max_length': '100', 'null': 'True', 'blank': 'True'})
        },
        'old.videorecordcollectivite': {
            'Meta': {'object_name': 'VideoRecordCollectivite', 'db_table': "u'video_record_collectivite'"},
            'collectivite': ('django.db.models.fields.related.ForeignKey', [], {'to': "orm['old.Collectivite']"}),
            'id': ('django.db.models.fields.IntegerField', [], {'primary_key': 'True'}),
            'video_record': ('django.db.models.fields.related.ForeignKey', [], {'to': "orm['old.VideoRecord']"})
        },
        'old.videorecordpersonnerole': {
            'Meta': {'object_name': 'VideoRecordPersonneRole', 'db_table': "u'video_record_personne_role'"},
            'id': ('django.db.models.fields.IntegerField', [], {'primary_key': 'True'}),
            'personne': ('django.db.models.fields.related.ForeignKey', [], {'to': "orm['old.Personne']"}),
            'role': ('django.db.models.fields.related.ForeignKey', [], {'to': "orm['old.Role']"}),
            'video_record': ('django.db.models.fields.related.ForeignKey', [], {'to': "orm['old.VideoRecord']"})
        },
        'old.videoset': {
            'Meta': {'object_name': 'VideoSet', 'db_table': "u'video_set'"},
            'date_debut': ('django.db.models.fields.DateField', [], {'null': 'True', 'blank': 'True'}),
            'date_fin': ('django.db.models.fields.DateField', [], {'null': 'True', 'blank': 'True'}),
            'id': ('django.db.models.fields.IntegerField', [], {'primary_key': 'True'}),
            'intitule': ('django.db.models.fields.CharField', [], {'max_length': '255'}),
            'notes': ('django.db.models.fields.TextField', [], {'null': 'True', 'blank': 'True'}),
            'parent': ('django.db.models.fields.related.ForeignKey', [], {'to': "orm['old.VideoSet']"}),
            'resume': ('django.db.models.fields.TextField', [], {'null': 'True', 'blank': 'True'}),
            'sous_titre': ('django.db.models.fields.CharField', [], {'max_length': '384', 'null': 'True', 'blank': 'True'}),
            'supprime': ('django.db.models.fields.IntegerField', [], {'default': '0'}),
            'time_stamp': ('django.db.models.fields.DateTimeField', [], {'auto_now': 'True', 'blank': 'True'})
        },
        'old.videovolume': {
            'Meta': {'object_name': 'VideoVolume', 'db_table': "u'video_volume'"},
            'date': ('django.db.models.fields.DateField', [], {'null': 'True', 'blank': 'True'}),
            'horaire': ('django.db.models.fields.CharField', [], {'default': 'None', 'max_length': '5', 'null': 'True', 'blank': 'True'}),
            'id': ('django.db.models.fields.CharField', [], {'max_length': '12', 'primary_key': 'True'}),
            'intitule': ('django.db.models.fields.TextField', [], {'null': 'True', 'blank': 'True'}),
            'lieu': ('django.db.models.fields.related.ForeignKey', [], {'to': "orm['old.Lieu']"}),
            'notes': ('django.db.models.fields.TextField', [], {'blank': 'True'}),
            'parent': ('django.db.models.fields.related.ForeignKey', [], {'to': "orm['old.Evenement']", 'null': 'True', 'blank': 'True'}),
            'resume': ('django.db.models.fields.TextField', [], {'null': 'True', 'blank': 'True'}),
            'sort': ('django.db.models.fields.CharField', [], {'default': 'None', 'max_length': '12', 'null': 'True', 'blank': 'True'}),
            'supprime': ('django.db.models.fields.IntegerField', [], {'default': '0'}),
            'technicien': ('django.db.models.fields.related.ForeignKey', [], {'to': "orm['old.Utilisateur']"}),
            'time_stamp': ('django.db.models.fields.DateTimeField', [], {'auto_now': 'True', 'blank': 'True'}),
            'type': ('django.db.models.fields.IntegerField', [], {'null': 'True', 'blank': 'True'})
        },
        'old.videovolumecollectivite': {
            'Meta': {'object_name': 'VideoVolumeCollectivite', 'db_table': "u'video_volume_collectivite'"},
            'collectivite': ('django.db.models.fields.related.ForeignKey', [], {'to': "orm['old.Collectivite']"}),
            'id': ('django.db.models.fields.IntegerField', [], {'primary_key': 'True'}),
            'video_volume': ('django.db.models.fields.related.ForeignKey', [], {'to': "orm['old.VideoVolume']"})
        },
        'old.videovolumepersonnerole': {
            'Meta': {'object_name': 'VideoVolumePersonneRole', 'db_table': "u'video_volume_personne_role'"},
            'id': ('django.db.models.fields.IntegerField', [], {'primary_key': 'True'}),
            'personne': ('django.db.models.fields.related.ForeignKey', [], {'to': "orm['old.Personne']"}),
            'role': ('django.db.models.fields.related.ForeignKey', [], {'to': "orm['old.Role']"}),
            'video_volume': ('django.db.models.fields.related.ForeignKey', [], {'to': "orm['old.VideoVolume']"})
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
            'lieu': ('django.db.models.fields.related.ForeignKey', [], {'to': "orm['old.Lieu']"}),
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