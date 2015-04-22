# -*- coding: utf-8 -*-
import datetime
from south.db import db
from south.v2 import DataMigration
from django.db import models

class Migration(DataMigration):

    def forwards(self, orm):
        "Write your forwards methods here."
        # Note: Remember to use orm['appname.ModelName'] rather than "from appname.models..."
        '''
        from old.models import Evenement #, Volume, NoteProgramme, TagEvenement
        video_volumes = orm.Volume.objects.all().exclude(parent_id=None)
        for video_volume in video_volumes:
            evt = Evenement.objects.get(id=video_volume.parent_id)
            tag_evenement_ids = evt.get_ancestors().exclude(flag_categorie=1).exclude(level=0).values_list('id', flat=True)
            if len(tag_evenement_ids) > 0:
                tag_evenements = orm.TagEvenement.objects.filter(id__in=tag_evenement_ids)
                video_volume.tag_evenements.add(*list(tag_evenements))
        '''
        video_volumes = orm.Volume.objects.all().exclude(parent_id=None)
        for video_volume in video_volumes:
            evt = orm.Evenement.objects.get(id=video_volume.parent_id)
            lft = evt.lft
            rght = evt.rght
            tree_id = evt.tree_id
            tag_evenement_ids = orm.Evenement.objects.filter(lft__lte=lft, rght__gte=rght, tree_id=tree_id)\
                .exclude(level=0).exclude(id=evt.id).values_list('id', flat=True)
            if len(tag_evenement_ids) > 0:
                tag_evenements = orm.TagEvenement.objects.filter(id__in=tag_evenement_ids)
                video_volume.tag_evenements.add(*list(tag_evenements))

    def backwards(self, orm):
        "Write your backwards methods here."
        pass

    models = {
        'old.collectivite': {
            'Meta': {'object_name': 'Collectivite', 'db_table': "u'collectivite'"},
            'forme_canonique': ('django.db.models.fields.related.ForeignKey', [], {'to': "orm['old.Collectivite']", 'null': 'True', 'blank': 'True'}),
            'id': ('django.db.models.fields.IntegerField', [], {'primary_key': 'True'}),
            'indice': ('django.db.models.fields.CharField', [], {'max_length': '2'}),
            'nom': ('django.db.models.fields.CharField', [], {'unique': 'True', 'max_length': '255'}),
            'supprime': ('django.db.models.fields.IntegerField', [], {'default': '0'})
        },
        'old.contrat': {
            'Meta': {'object_name': 'Contrat', 'db_table': "u'contrat'"},
            'contract': ('django.db.models.fields.files.FileField', [], {'max_length': '100', 'null': 'True', 'blank': 'True'}),
            'id': ('django.db.models.fields.IntegerField', [], {'primary_key': 'True'}),
            'intitule': ('django.db.models.fields.CharField', [], {'max_length': '255'}),
            'mime_type': ('django.db.models.fields.CharField', [], {'max_length': '765', 'null': 'True', 'blank': 'True'}),
            'notes': ('django.db.models.fields.TextField', [], {'null': 'True', 'blank': 'True'}),
            'num_pages': ('django.db.models.fields.IntegerField', [], {'null': 'True', 'blank': 'True'}),
            'parent': ('django.db.models.fields.related.ForeignKey', [], {'to': "orm['old.VideoVolume']"}),
            'supprime': ('django.db.models.fields.IntegerField', [], {'default': '0'}),
            'technicien': ('django.db.models.fields.related.ForeignKey', [], {'to': "orm['old.Utilisateur']"}),
            'time_stamp': ('django.db.models.fields.DateTimeField', [], {'auto_now': 'True', 'blank': 'True'}),
            'type': ('django.db.models.fields.CharField', [], {'max_length': '1'})
        },
        'old.evenement': {
            'Meta': {'object_name': 'Evenement', 'db_table': "u'evenement'"},
            'audio_children': ('django.db.models.fields.IntegerField', [], {'null': 'True', 'blank': 'True'}),
            'date_debut': ('django.db.models.fields.DateField', [], {'null': 'True', 'blank': 'True'}),
            'date_fin': ('django.db.models.fields.DateField', [], {'null': 'True', 'blank': 'True'}),
            'event_children': ('django.db.models.fields.IntegerField', [], {'null': 'True', 'blank': 'True'}),
            'flag_archive': ('django.db.models.fields.BooleanField', [], {'default': 'False'}),
            'flag_categorie': ('django.db.models.fields.BooleanField', [], {'default': 'False'}),
            'id': ('django.db.models.fields.IntegerField', [], {'primary_key': 'True'}),
            'intitule': ('django.db.models.fields.CharField', [], {'unique': 'True', 'max_length': '255'}),
            'level': ('django.db.models.fields.PositiveIntegerField', [], {'db_index': 'True'}),
            'lft': ('django.db.models.fields.PositiveIntegerField', [], {'db_index': 'True'}),
            'notes': ('django.db.models.fields.TextField', [], {'null': 'True', 'blank': 'True'}),
            'parent': ('mptt.fields.TreeForeignKey', [], {'blank': 'True', 'related_name': "'children'", 'null': 'True', 'to': "orm['old.Evenement']"}),
            'pdf_children': ('django.db.models.fields.IntegerField', [], {'null': 'True', 'blank': 'True'}),
            'resume': ('django.db.models.fields.TextField', [], {'null': 'True', 'blank': 'True'}),
            'rght': ('django.db.models.fields.PositiveIntegerField', [], {'db_index': 'True'}),
            'sous_titre': ('django.db.models.fields.CharField', [], {'max_length': '384', 'null': 'True', 'blank': 'True'}),
            'supprime': ('django.db.models.fields.IntegerField', [], {'default': '0'}),
            'time_stamp': ('django.db.models.fields.DateTimeField', [], {'auto_now': 'True', 'blank': 'True'}),
            'tree_id': ('django.db.models.fields.PositiveIntegerField', [], {'db_index': 'True'}),
            'type': ('django.db.models.fields.related.ForeignKey', [], {'to': "orm['old.TypeEvenement']", 'null': 'True', 'blank': 'True'}),
            'video_children': ('django.db.models.fields.IntegerField', [], {'null': 'True', 'blank': 'True'})
        },
        'old.lieu': {
            'Meta': {'object_name': 'Lieu', 'db_table': "u'lieu'"},
            'id': ('django.db.models.fields.IntegerField', [], {'primary_key': 'True'}),
            'nom': ('django.db.models.fields.CharField', [], {'unique': 'True', 'max_length': '255'}),
            'pays': ('django.db.models.fields.CharField', [], {'max_length': '765'}),
            'salle': ('django.db.models.fields.CharField', [], {'max_length': '255', 'null': 'True', 'blank': 'True'}),
            'supprime': ('django.db.models.fields.IntegerField', [], {'default': '0'}),
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
            'confidentialite': ('django.db.models.fields.CharField', [], {'max_length': '1'}),
            'date_transfert': ('django.db.models.fields.DateField', [], {'null': 'True', 'blank': 'True'}),
            'editeur': ('django.db.models.fields.related.ForeignKey', [], {'to': "orm['old.Collectivite']", 'null': 'True', 'blank': 'True'}),
            'etat_note': ('django.db.models.fields.CharField', [], {'max_length': '1'}),
            'id': ('django.db.models.fields.IntegerField', [], {'primary_key': 'True'}),
            'id_loris': ('django.db.models.fields.CharField', [], {'unique': 'True', 'max_length': '15'}),
            'intitule': ('django.db.models.fields.CharField', [], {'max_length': '255'}),
            'mime_type': ('django.db.models.fields.CharField', [], {'max_length': '765', 'null': 'True', 'blank': 'True'}),
            'notes': ('django.db.models.fields.TextField', [], {'null': 'True', 'blank': 'True'}),
            'num_pages': ('django.db.models.fields.IntegerField', [], {'null': 'True', 'blank': 'True'}),
            'parent': ('django.db.models.fields.related.ForeignKey', [], {'to': "orm['old.Evenement']"}),
            'program': ('django.db.models.fields.files.FileField', [], {'max_length': '100', 'null': 'True', 'blank': 'True'}),
            'program_ext': ('django.db.models.fields.files.FileField', [], {'max_length': '100', 'null': 'True', 'blank': 'True'}),
            'program_int': ('django.db.models.fields.files.FileField', [], {'max_length': '100', 'null': 'True', 'blank': 'True'}),
            'saison': ('django.db.models.fields.related.ForeignKey', [], {'to': "orm['old.Saison']", 'null': 'True', 'blank': 'True'}),
            'sous_titre': ('django.db.models.fields.CharField', [], {'max_length': '384', 'null': 'True', 'blank': 'True'}),
            'supprime': ('django.db.models.fields.IntegerField', [], {'default': '0'}),
            'tag_evenements': ('django.db.models.fields.related.ManyToManyField', [], {'symmetrical': 'False', 'to': "orm['old.TagEvenement']", 'null': 'True', 'blank': 'True'}),
            'technicien': ('django.db.models.fields.related.ForeignKey', [], {'to': "orm['old.Utilisateur']"}),
            'time_stamp': ('django.db.models.fields.DateTimeField', [], {'auto_now': 'True', 'blank': 'True'}),
            'type_evenement': ('django.db.models.fields.related.ForeignKey', [], {'to': "orm['old.TypeEvenement']", 'null': 'True', 'blank': 'True'})
        },
        'old.oeuvre': {
            'Meta': {'object_name': 'Oeuvre', 'db_table': "u'oeuvre'"},
            'annee': ('django.db.models.fields.CharField', [], {'max_length': '12', 'null': 'True', 'blank': 'True'}),
            'id': ('django.db.models.fields.IntegerField', [], {'primary_key': 'True'}),
            'sous_titre': ('django.db.models.fields.CharField', [], {'max_length': '384', 'null': 'True', 'blank': 'True'}),
            'supprime': ('django.db.models.fields.IntegerField', [], {'default': '0'}),
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
            'brahms_key': ('django.db.models.fields.CharField', [], {'max_length': '27', 'null': 'True', 'blank': 'True'}),
            'confidentialite_partie': ('django.db.models.fields.CharField', [], {'max_length': '1'}),
            'doris_key': ('django.db.models.fields.IntegerField', [], {'default': '0'}),
            'duree': ('django.db.models.fields.TextField', [], {'null': 'True', 'blank': 'True'}),
            'editeur_partition': ('django.db.models.fields.related.ForeignKey', [], {'to': "orm['old.Collectivite']", 'null': 'True', 'blank': 'True'}),
            'id': ('django.db.models.fields.CharField', [], {'max_length': '36', 'primary_key': 'True'}),
            'notes': ('django.db.models.fields.CharField', [], {'max_length': '765', 'null': 'True', 'blank': 'True'}),
            'oeuvre': ('django.db.models.fields.related.ForeignKey', [], {'to': "orm['old.Oeuvre']", 'null': 'True', 'blank': 'True'}),
            'partype': ('django.db.models.fields.CharField', [], {'max_length': '1'}),
            'resume': ('django.db.models.fields.TextField', [], {'null': 'True', 'blank': 'True'}),
            'seq': ('django.db.models.fields.IntegerField', [], {}),
            'supprime': ('django.db.models.fields.IntegerField', [], {'default': '0'}),
            'time_stamp': ('django.db.models.fields.DateTimeField', [], {'auto_now': 'True', 'blank': 'True'}),
            'titre': ('django.db.models.fields.TextField', [], {'null': 'True', 'blank': 'True'}),
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
            'indice': ('django.db.models.fields.CharField', [], {'max_length': '2'}),
            'nom': ('django.db.models.fields.CharField', [], {'max_length': '150'}),
            'prenom': ('django.db.models.fields.CharField', [], {'max_length': '150'}),
            'supprime': ('django.db.models.fields.IntegerField', [], {})
        },
        'old.role': {
            'Meta': {'object_name': 'Role', 'db_table': "u'role'"},
            'forme_canonique': ('django.db.models.fields.related.ForeignKey', [], {'to': "orm['old.Role']", 'null': 'True', 'blank': 'True'}),
            'id': ('django.db.models.fields.IntegerField', [], {'primary_key': 'True'}),
            'indice': ('django.db.models.fields.CharField', [], {'max_length': '2'}),
            'intitule': ('django.db.models.fields.CharField', [], {'unique': 'True', 'max_length': '255'}),
            'supprime': ('django.db.models.fields.IntegerField', [], {'default': '0'})
        },
        'old.saison': {
            'Meta': {'object_name': 'Saison', 'db_table': "u'saison'"},
            'date_debut': ('django.db.models.fields.DateField', [], {'null': 'True', 'blank': 'True'}),
            'date_fin': ('django.db.models.fields.DateField', [], {'null': 'True', 'blank': 'True'}),
            'id': ('django.db.models.fields.IntegerField', [], {'primary_key': 'True'}),
            'intitule': ('django.db.models.fields.CharField', [], {'unique': 'True', 'max_length': '255'}),
            'sous_titre': ('django.db.models.fields.CharField', [], {'max_length': '384', 'null': 'True', 'blank': 'True'}),
            'time_stamp': ('django.db.models.fields.DateTimeField', [], {'auto_now': 'True', 'blank': 'True'})
        },
        'old.tagevenement': {
            'Meta': {'object_name': 'TagEvenement', 'db_table': "u'tag_evenement'"},
            'date_debut': ('django.db.models.fields.DateField', [], {'null': 'True', 'blank': 'True'}),
            'date_fin': ('django.db.models.fields.DateField', [], {'null': 'True', 'blank': 'True'}),
            'id': ('django.db.models.fields.IntegerField', [], {'primary_key': 'True'}),
            'intitule': ('django.db.models.fields.CharField', [], {'max_length': '255'}),
            'sous_titre': ('django.db.models.fields.CharField', [], {'max_length': '384', 'null': 'True', 'blank': 'True'}),
            'time_stamp': ('django.db.models.fields.DateTimeField', [], {'auto_now': 'True', 'blank': 'True'})
        },
        'old.typeevenement': {
            'Meta': {'object_name': 'TypeEvenement', 'db_table': "u'type_evenement'"},
            'id': ('django.db.models.fields.IntegerField', [], {'primary_key': 'True'}),
            'intitule': ('django.db.models.fields.CharField', [], {'unique': 'True', 'max_length': '255'}),
            'supprime': ('django.db.models.fields.IntegerField', [], {'default': '0'})
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
            'mime_type': ('django.db.models.fields.CharField', [], {'max_length': '192', 'null': 'True', 'blank': 'True'}),
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
            'parent': ('django.db.models.fields.related.ForeignKey', [], {'to': "orm['old.VideoSet']", 'null': 'True', 'blank': 'True'}),
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
            'lieu': ('django.db.models.fields.related.ForeignKey', [], {'to': "orm['old.Lieu']", 'null': 'True', 'blank': 'True'}),
            'notes': ('django.db.models.fields.TextField', [], {'blank': 'True'}),
            'parent': ('django.db.models.fields.related.ForeignKey', [], {'to': "orm['old.Evenement']", 'null': 'True', 'blank': 'True'}),
            'resume': ('django.db.models.fields.TextField', [], {'null': 'True', 'blank': 'True'}),
            'saison': ('django.db.models.fields.related.ForeignKey', [], {'to': "orm['old.Saison']", 'null': 'True', 'blank': 'True'}),
            'sort': ('django.db.models.fields.CharField', [], {'default': 'None', 'max_length': '12', 'null': 'True', 'blank': 'True'}),
            'sous_titre': ('django.db.models.fields.CharField', [], {'max_length': '384', 'null': 'True', 'blank': 'True'}),
            'supprime': ('django.db.models.fields.IntegerField', [], {'default': '0'}),
            'tag_evenements': ('django.db.models.fields.related.ManyToManyField', [], {'symmetrical': 'False', 'to': "orm['old.TagEvenement']", 'null': 'True', 'blank': 'True'}),
            'technicien': ('django.db.models.fields.related.ForeignKey', [], {'to': "orm['old.Utilisateur']", 'null': 'True', 'blank': 'True'}),
            'time_stamp': ('django.db.models.fields.DateTimeField', [], {'auto_now': 'True', 'blank': 'True'}),
            'type': ('django.db.models.fields.CharField', [], {'max_length': '1', 'null': 'True', 'blank': 'True'}),
            'type_evenement': ('django.db.models.fields.related.ForeignKey', [], {'to': "orm['old.TypeEvenement']", 'null': 'True', 'blank': 'True'})
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
            'annee': ('django.db.models.fields.TextField', [], {'null': 'True', 'blank': 'True'}),
            'auteur': ('django.db.models.fields.TextField', [], {'null': 'True', 'blank': 'True'}),
            'cddb': ('django.db.models.fields.CharField', [], {'max_length': '24', 'null': 'True', 'db_column': "'CDDB'", 'blank': 'True'}),
            'confidentialite_volume': ('django.db.models.fields.CharField', [], {'max_length': '1'}),
            'date': ('django.db.models.fields.DateField', [], {'null': 'True', 'blank': 'True'}),
            'date_transfert': ('django.db.models.fields.DateField', [], {'null': 'True', 'blank': 'True'}),
            'doris_key': ('django.db.models.fields.IntegerField', [], {'default': '0'}),
            'etat_archive': ('django.db.models.fields.CharField', [], {'max_length': '1'}),
            'etat_collection': ('django.db.models.fields.CharField', [], {'max_length': '1'}),
            'horaire': ('django.db.models.fields.CharField', [], {'max_length': '15'}),
            'id': ('django.db.models.fields.CharField', [], {'max_length': '36', 'primary_key': 'True'}),
            'intitule': ('django.db.models.fields.TextField', [], {'null': 'True', 'blank': 'True'}),
            'label': ('django.db.models.fields.TextField', [], {'null': 'True', 'blank': 'True'}),
            'lieu': ('django.db.models.fields.related.ForeignKey', [], {'to': "orm['old.Lieu']", 'null': 'True', 'blank': 'True'}),
            'note2prog_id': ('django.db.models.fields.CharField', [], {'max_length': '30', 'null': 'True', 'blank': 'True'}),
            'notes': ('django.db.models.fields.TextField', [], {'null': 'True', 'blank': 'True'}),
            'old_id': ('django.db.models.fields.CharField', [], {'max_length': '384', 'null': 'True', 'blank': 'True'}),
            'parent': ('django.db.models.fields.related.ForeignKey', [], {'to': "orm['old.Evenement']", 'null': 'True', 'blank': 'True'}),
            'pending': ('django.db.models.fields.CharField', [], {'max_length': '1'}),
            'pret': ('django.db.models.fields.CharField', [], {'max_length': '1'}),
            'resume': ('django.db.models.fields.TextField', [], {'null': 'True', 'blank': 'True'}),
            'saison': ('django.db.models.fields.related.ForeignKey', [], {'to': "orm['old.Saison']", 'null': 'True', 'blank': 'True'}),
            'sous_titre': ('django.db.models.fields.CharField', [], {'max_length': '384', 'null': 'True', 'blank': 'True'}),
            'supprime': ('django.db.models.fields.IntegerField', [], {'default': '0'}),
            'tag_evenements': ('django.db.models.fields.related.ManyToManyField', [], {'symmetrical': 'False', 'to': "orm['old.TagEvenement']", 'null': 'True', 'blank': 'True'}),
            'technicien': ('django.db.models.fields.related.ForeignKey', [], {'to': "orm['old.Utilisateur']", 'null': 'True', 'blank': 'True'}),
            'time_stamp': ('django.db.models.fields.DateTimeField', [], {'auto_now': 'True', 'blank': 'True'}),
            'type_evenement': ('django.db.models.fields.related.ForeignKey', [], {'to': "orm['old.TypeEvenement']", 'null': 'True', 'blank': 'True'}),
            'url': ('django.db.models.fields.TextField', [], {'null': 'True', 'blank': 'True'}),
            'voltype': ('django.db.models.fields.CharField', [], {'max_length': '1'})
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
    symmetrical = True
