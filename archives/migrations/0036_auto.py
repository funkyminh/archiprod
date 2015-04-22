# -*- coding: utf-8 -*-
import datetime
from south.db import db
from south.v2 import SchemaMigration
from django.db import models


class Migration(SchemaMigration):

    def forwards(self, orm):
        # Adding M2M table for field role_new on 'Participant'
        db.create_table(u'archives_participant_role_new', (
            ('id', models.AutoField(verbose_name='ID', primary_key=True, auto_created=True)),
            ('participant', models.ForeignKey(orm[u'archives.participant'], null=False)),
            ('role', models.ForeignKey(orm[u'utils.role'], null=False))
        ))
        db.create_unique(u'archives_participant_role_new', ['participant_id', 'role_id'])

        # Adding M2M table for field role_new on 'ArchiveParticipant'
        db.create_table(u'archives_archiveparticipant_role_new', (
            ('id', models.AutoField(verbose_name='ID', primary_key=True, auto_created=True)),
            ('archiveparticipant', models.ForeignKey(orm[u'archives.archiveparticipant'], null=False)),
            ('role', models.ForeignKey(orm[u'utils.role'], null=False))
        ))
        db.create_unique(u'archives_archiveparticipant_role_new', ['archiveparticipant_id', 'role_id'])

        # Adding M2M table for field role_new on 'MediaCollectivity'
        db.create_table('archives_media_collectivities_role_new', (
            ('id', models.AutoField(verbose_name='ID', primary_key=True, auto_created=True)),
            ('mediacollectivity', models.ForeignKey(orm[u'archives.mediacollectivity'], null=False)),
            ('role', models.ForeignKey(orm[u'utils.role'], null=False))
        ))
        db.create_unique('archives_media_collectivities_role_new', ['mediacollectivity_id', 'role_id'])

        # Adding M2M table for field role_new on 'ArchiveCollectivity'
        db.create_table('archives_archive_collectivities_role_new', (
            ('id', models.AutoField(verbose_name='ID', primary_key=True, auto_created=True)),
            ('archivecollectivity', models.ForeignKey(orm[u'archives.archivecollectivity'], null=False)),
            ('role', models.ForeignKey(orm[u'utils.role'], null=False))
        ))
        db.create_unique('archives_archive_collectivities_role_new', ['archivecollectivity_id', 'role_id'])


    def backwards(self, orm):
        # Removing M2M table for field role_new on 'Participant'
        db.delete_table('archives_participant_role_new')

        # Removing M2M table for field role_new on 'ArchiveParticipant'
        db.delete_table('archives_archiveparticipant_role_new')

        # Removing M2M table for field role_new on 'MediaCollectivity'
        db.delete_table('archives_media_collectivities_role_new')

        # Removing M2M table for field role_new on 'ArchiveCollectivity'
        db.delete_table('archives_archive_collectivities_role_new')


    models = {
        u'archives.archive': {
            'Meta': {'object_name': 'Archive'},
            'available': ('django.db.models.fields.CharField', [], {'max_length': '1', 'null': 'True', 'blank': 'True'}),
            'collectivities': ('django.db.models.fields.related.ManyToManyField', [], {'symmetrical': 'False', 'to': u"orm['utils.Collectivity']", 'null': 'True', 'through': u"orm['archives.ArchiveCollectivity']", 'blank': 'True'}),
            'comments': ('django.db.models.fields.TextField', [], {'null': 'True', 'blank': 'True'}),
            'date': ('django.db.models.fields.DateField', [], {'null': 'True', 'blank': 'True'}),
            'date_transfert': ('django.db.models.fields.DateField', [], {'null': 'True', 'blank': 'True'}),
            'event': ('django.db.models.fields.related.ForeignKey', [], {'to': u"orm['events.Event']", 'null': 'True', 'blank': 'True'}),
            u'id': ('django.db.models.fields.AutoField', [], {'primary_key': 'True'}),
            'id_archiprod': ('django.db.models.fields.CharField', [], {'max_length': '12'}),
            'note2prog_id': ('django.db.models.fields.CharField', [], {'max_length': '30', 'null': 'True', 'blank': 'True'}),
            'old_id': ('django.db.models.fields.CharField', [], {'max_length': '384', 'null': 'True', 'blank': 'True'}),
            'order': ('django.db.models.fields.CharField', [], {'default': 'None', 'max_length': '12', 'null': 'True', 'blank': 'True'}),
            'participants': ('django.db.models.fields.related.ManyToManyField', [], {'symmetrical': 'False', 'to': u"orm['utils.Person']", 'null': 'True', 'through': u"orm['archives.ArchiveParticipant']", 'blank': 'True'}),
            'pending': ('django.db.models.fields.CharField', [], {'max_length': '1', 'null': 'True', 'blank': 'True'}),
            'place': ('django.db.models.fields.related.ForeignKey', [], {'to': u"orm['utils.Place']", 'null': 'True', 'blank': 'True'}),
            'reviewer': ('django.db.models.fields.related.ForeignKey', [], {'blank': 'True', 'related_name': "'reviewer'", 'null': 'True', 'to': u"orm['auth.User']"}),
            'set': ('django.db.models.fields.related.ForeignKey', [], {'to': u"orm['archives.Set']", 'null': 'True', 'blank': 'True'}),
            'state': ('django.db.models.fields.CharField', [], {'max_length': '1', 'null': 'True', 'blank': 'True'}),
            'subtitle': ('django.db.models.fields.CharField', [], {'max_length': '384', 'null': 'True', 'blank': 'True'}),
            'summary': ('django.db.models.fields.TextField', [], {'null': 'True', 'blank': 'True'}),
            'tags': ('django.db.models.fields.related.ManyToManyField', [], {'symmetrical': 'False', 'to': u"orm['archives.Tag']", 'null': 'True', 'blank': 'True'}),
            'time': ('django.db.models.fields.TimeField', [], {'null': 'True', 'blank': 'True'}),
            'time_stamp': ('django.db.models.fields.DateTimeField', [], {'auto_now': 'True', 'blank': 'True'}),
            'title': ('django.db.models.fields.CharField', [], {'max_length': '255', 'null': 'True', 'blank': 'True'}),
            'user': ('django.db.models.fields.related.ForeignKey', [], {'to': u"orm['auth.User']", 'null': 'True', 'blank': 'True'})
        },
        u'archives.archivecollectivity': {
            'Meta': {'unique_together': "(('archive', 'collectivity'),)", 'object_name': 'ArchiveCollectivity', 'db_table': "'archives_archive_collectivities'"},
            'archive': ('django.db.models.fields.related.ForeignKey', [], {'to': u"orm['archives.Archive']"}),
            'collectivity': ('django.db.models.fields.related.ForeignKey', [], {'to': u"orm['utils.Collectivity']"}),
            u'id': ('django.db.models.fields.AutoField', [], {'primary_key': 'True'}),
            'role': ('django.db.models.fields.related.ForeignKey', [], {'to': u"orm['utils.Role']", 'null': 'True', 'blank': 'True'}),
            'role_new': ('django.db.models.fields.related.ManyToManyField', [], {'blank': 'True', 'related_name': "'role_new3'", 'null': 'True', 'symmetrical': 'False', 'to': u"orm['utils.Role']"})
        },
        u'archives.archiveparticipant': {
            'Meta': {'object_name': 'ArchiveParticipant'},
            'archive': ('django.db.models.fields.related.ForeignKey', [], {'to': u"orm['archives.Archive']"}),
            u'id': ('django.db.models.fields.AutoField', [], {'primary_key': 'True'}),
            'person': ('django.db.models.fields.related.ForeignKey', [], {'to': u"orm['utils.Person']"}),
            'role': ('django.db.models.fields.related.ForeignKey', [], {'to': u"orm['utils.Role']"}),
            'role_new': ('django.db.models.fields.related.ManyToManyField', [], {'blank': 'True', 'related_name': "'role_new1'", 'null': 'True', 'symmetrical': 'False', 'to': u"orm['utils.Role']"})
        },
        u'archives.audio': {
            'Meta': {'object_name': 'Audio', 'db_table': "u'audio'"},
            'abstract': ('django.db.models.fields.TextField', [], {'blank': 'True'}),
            'acanthes': ('django.db.models.fields.TextField', [], {'blank': 'True'}),
            'annee': ('django.db.models.fields.CharField', [], {'max_length': '255', 'blank': 'True'}),
            'chemin_fichier': ('django.db.models.fields.TextField', [], {'blank': 'True'}),
            'date_enregistrement': ('django.db.models.fields.TextField', [], {'blank': 'True'}),
            'dateissued_portail': ('django.db.models.fields.TextField', [], {'db_column': "'dateIssued_portail'", 'blank': 'True'}),
            'details_intranet_actuel_acda': ('django.db.models.fields.TextField', [], {'db_column': "'details_intranet_actuel_ACDA'", 'blank': 'True'}),
            'duree': ('django.db.models.fields.TextField', [], {'blank': 'True'}),
            'genre': ('django.db.models.fields.CharField', [], {'max_length': '255', 'blank': 'True'}),
            'horodatage_creation': ('django.db.models.fields.TextField', [], {'blank': 'True'}),
            'horodatage_modification': ('django.db.models.fields.TextField', [], {'blank': 'True'}),
            u'id': ('django.db.models.fields.AutoField', [], {'primary_key': 'True'}),
            'intervenants': ('django.db.models.fields.related.ManyToManyField', [], {'related_name': "'intervenants_audio'", 'symmetrical': 'False', 'through': u"orm['archives.IntervenantAudio']", 'to': u"orm['archives.Intervenant']"}),
            'kf_id_intervenant_principal': ('django.db.models.fields.related.ForeignKey', [], {'to': u"orm['archives.Intervenant']", 'null': 'True', 'db_column': "'kf_ID_intervenant_principal'", 'blank': 'True'}),
            'kf_id_langue_1': ('django.db.models.fields.related.ForeignKey', [], {'blank': 'True', 'related_name': "'langue_1'", 'null': 'True', 'db_column': "'kf_ID_langue_1'", 'to': u"orm['archives.Langue']"}),
            'kf_id_langue_2': ('django.db.models.fields.related.ForeignKey', [], {'blank': 'True', 'related_name': "'langue_2'", 'null': 'True', 'db_column': "'kf_ID_langue_2'", 'to': u"orm['archives.Langue']"}),
            'kf_id_langue_3': ('django.db.models.fields.related.ForeignKey', [], {'blank': 'True', 'related_name': "'langue_3'", 'null': 'True', 'db_column': "'kf_ID_langue_3'", 'to': u"orm['archives.Langue']"}),
            'kf_id_lieu': ('django.db.models.fields.related.ForeignKey', [], {'to': u"orm['archives.Lieu']", 'null': 'True', 'db_column': "'kf_ID_lieu'", 'blank': 'True'}),
            'kf_id_orchestre': ('django.db.models.fields.related.ForeignKey', [], {'to': u"orm['archives.Orchestre']", 'null': 'True', 'db_column': "'kf_ID_orchestre'", 'blank': 'True'}),
            'lien_test_web': ('django.db.models.fields.TextField', [], {'blank': 'True'}),
            'oai_abstract': ('django.db.models.fields.TextField', [], {'blank': 'True'}),
            'oai_accesscondition': ('django.db.models.fields.TextField', [], {'db_column': "'oai_accessCondition'", 'blank': 'True'}),
            'oai_genre': ('django.db.models.fields.TextField', [], {'blank': 'True'}),
            'oai_id': ('django.db.models.fields.TextField', [], {'blank': 'True'}),
            'oai_language_languageterm_1': ('django.db.models.fields.TextField', [], {'db_column': "'oai_language_languageTerm_1'", 'blank': 'True'}),
            'oai_language_languageterm_2': ('django.db.models.fields.TextField', [], {'db_column': "'oai_language_languageTerm_2'", 'blank': 'True'}),
            'oai_language_languageterm_3': ('django.db.models.fields.TextField', [], {'db_column': "'oai_language_languageTerm_3'", 'blank': 'True'}),
            'oai_location_physicallocation': ('django.db.models.fields.TextField', [], {'db_column': "'oai_location_physicalLocation'", 'blank': 'True'}),
            'oai_location_url_full': ('django.db.models.fields.TextField', [], {'blank': 'True'}),
            'oai_location_url_preview': ('django.db.models.fields.TextField', [], {'blank': 'True'}),
            'oai_origininfo_datecaptured': ('django.db.models.fields.TextField', [], {'db_column': "'oai_originInfo_dateCaptured'", 'blank': 'True'}),
            'oai_origininfo_place': ('django.db.models.fields.TextField', [], {'db_column': "'oai_originInfo_place'", 'blank': 'True'}),
            'oai_origininfo_publisher': ('django.db.models.fields.TextField', [], {'db_column': "'oai_originInfo_publisher'", 'blank': 'True'}),
            'oai_physicaldescription_digitalorigin': ('django.db.models.fields.TextField', [], {'db_column': "'oai_physicalDescription_digitalOrigin'", 'blank': 'True'}),
            'oai_physicaldescription_form': ('django.db.models.fields.TextField', [], {'db_column': "'oai_physicalDescription_form'", 'blank': 'True'}),
            'oai_physicaldescription_internetmediatype': ('django.db.models.fields.TextField', [], {'db_column': "'oai_physicalDescription_internetMediaType'", 'blank': 'True'}),
            'oai_publication': ('django.db.models.fields.TextField', [], {'blank': 'True'}),
            'oai_recordinfo_languageofcataloging_languageterm': ('django.db.models.fields.TextField', [], {'db_column': "'oai_recordInfo_languageOfCataloging_languageTerm'", 'blank': 'True'}),
            'oai_recordinfo_recordchangedate': ('django.db.models.fields.TextField', [], {'db_column': "'oai_recordInfo_recordChangeDate'", 'blank': 'True'}),
            'oai_recordinfo_recordcontentsource': ('django.db.models.fields.TextField', [], {'db_column': "'oai_recordInfo_recordContentSource'", 'blank': 'True'}),
            'oai_recordinfo_recordcreationdate': ('django.db.models.fields.TextField', [], {'db_column': "'oai_recordInfo_recordCreationDate'", 'blank': 'True'}),
            'oai_recordinfo_recordidentifier': ('django.db.models.fields.TextField', [], {'db_column': "'oai_recordInfo_recordIdentifier'", 'blank': 'True'}),
            'oai_targetaudience': ('django.db.models.fields.TextField', [], {'db_column': "'oai_targetAudience'", 'blank': 'True'}),
            'oai_titleinfo_title': ('django.db.models.fields.TextField', [], {'db_column': "'oai_titleInfo_title'", 'blank': 'True'}),
            'oai_typeofresource': ('django.db.models.fields.TextField', [], {'db_column': "'oai_typeOfResource'", 'blank': 'True'}),
            'oai_web_oai_mods': ('django.db.models.fields.TextField', [], {'db_column': "'oai_WEB_OAI_MODS'", 'blank': 'True'}),
            'physicaldescription': ('django.db.models.fields.CharField', [], {'max_length': '255', 'db_column': "'physicalDescription'", 'blank': 'True'}),
            'remarque': ('django.db.models.fields.TextField', [], {'blank': 'True'}),
            'subtitle': ('django.db.models.fields.TextField', [], {'db_column': "'subTitle'", 'blank': 'True'}),
            'total_durees': ('django.db.models.fields.TextField', [], {'blank': 'True'}),
            'type_document': ('django.db.models.fields.CharField', [], {'max_length': '255', 'blank': 'True'}),
            'type_ircam': ('django.db.models.fields.TextField', [], {'blank': 'True'}),
            'typeofresource': ('django.db.models.fields.CharField', [], {'max_length': '255', 'null': 'True', 'db_column': "'typeOfResource'", 'blank': 'True'}),
            'url_ecoute_extranet': ('django.db.models.fields.TextField', [], {'blank': 'True'}),
            'url_ecoute_internet': ('django.db.models.fields.TextField', [], {'blank': 'True'}),
            'url_ecoute_intranet': ('django.db.models.fields.TextField', [], {'blank': 'True'}),
            'url_ecoute_intranet_adresse': ('django.db.models.fields.files.FileField', [], {'max_length': '100', 'blank': 'True'}),
            'url_export_ircam': ('django.db.models.fields.TextField', [], {'db_column': "'url_export IRCAM'", 'blank': 'True'})
        },
        u'archives.contract': {
            'Meta': {'object_name': 'Contract'},
            'archive': ('django.db.models.fields.related.ForeignKey', [], {'to': u"orm['archives.Archive']"}),
            'comments': ('django.db.models.fields.TextField', [], {'null': 'True', 'blank': 'True'}),
            'file': ('django.db.models.fields.files.FileField', [], {'max_length': '100', 'null': 'True', 'blank': 'True'}),
            u'id': ('django.db.models.fields.AutoField', [], {'primary_key': 'True'}),
            'nb_pages': ('django.db.models.fields.IntegerField', [], {'null': 'True', 'blank': 'True'}),
            'time_stamp': ('django.db.models.fields.DateTimeField', [], {'auto_now': 'True', 'blank': 'True'}),
            'title': ('django.db.models.fields.CharField', [], {'max_length': '255'}),
            'user': ('django.db.models.fields.related.ForeignKey', [], {'to': u"orm['auth.User']"})
        },
        u'archives.intervenant': {
            'Meta': {'object_name': 'Intervenant', 'db_table': "u'intervenant'"},
            'biographie': ('django.db.models.fields.TextField', [], {'blank': 'True'}),
            'horodatage_creation': ('django.db.models.fields.TextField', [], {'blank': 'True'}),
            'horodatage_modification': ('django.db.models.fields.TextField', [], {'blank': 'True'}),
            u'id': ('django.db.models.fields.AutoField', [], {'primary_key': 'True'}),
            'nom': ('django.db.models.fields.CharField', [], {'max_length': '255', 'db_column': "'Nom'", 'blank': 'True'}),
            'prenom': ('django.db.models.fields.CharField', [], {'max_length': '255', 'db_column': "u'Pr\\xe9nom'", 'blank': 'True'}),
            'prenom_nom': ('django.db.models.fields.CharField', [], {'max_length': '255', 'blank': 'True'}),
            'web_1': ('django.db.models.fields.CharField', [], {'max_length': '255', 'blank': 'True'}),
            'web_2': ('django.db.models.fields.CharField', [], {'max_length': '255', 'blank': 'True'})
        },
        u'archives.intervenantaudio': {
            'Meta': {'object_name': 'IntervenantAudio'},
            'audio': ('django.db.models.fields.related.ForeignKey', [], {'to': u"orm['archives.Audio']"}),
            u'id': ('django.db.models.fields.AutoField', [], {'primary_key': 'True'}),
            'intervenant': ('django.db.models.fields.related.ForeignKey', [], {'to': u"orm['archives.Intervenant']"}),
            'ordre': ('django.db.models.fields.IntegerField', [], {'null': 'True', 'blank': 'True'}),
            'role': ('django.db.models.fields.CharField', [], {'max_length': '255', 'null': 'True', 'blank': 'True'})
        },
        u'archives.langue': {
            'Meta': {'object_name': 'Langue', 'db_table': "u'langue'"},
            u'id': ('django.db.models.fields.AutoField', [], {'primary_key': 'True'}),
            'languageterm': ('django.db.models.fields.CharField', [], {'max_length': '255', 'db_column': "'languageTerm'", 'blank': 'True'})
        },
        u'archives.lieu': {
            'Meta': {'object_name': 'Lieu', 'db_table': "u'lieu'"},
            u'id': ('django.db.models.fields.AutoField', [], {'primary_key': 'True'}),
            'placeterm': ('django.db.models.fields.CharField', [], {'max_length': "'255'", 'db_column': "'placeTerm'", 'blank': 'True'}),
            'salle': ('django.db.models.fields.CharField', [], {'max_length': "'255'", 'blank': 'True'})
        },
        u'archives.media': {
            'Meta': {'object_name': 'Media'},
            'archive': ('django.db.models.fields.related.ForeignKey', [], {'to': u"orm['archives.Archive']", 'null': 'True', 'blank': 'True'}),
            'collectivities': ('django.db.models.fields.related.ManyToManyField', [], {'symmetrical': 'False', 'to': u"orm['utils.Collectivity']", 'null': 'True', 'through': u"orm['archives.MediaCollectivity']", 'blank': 'True'}),
            'comments': ('django.db.models.fields.TextField', [], {'null': 'True', 'blank': 'True'}),
            'confidentiality': ('django.db.models.fields.CharField', [], {'default': "'0'", 'max_length': '1'}),
            'duration': ('django.db.models.fields.TimeField', [], {'null': 'True', 'blank': 'True'}),
            'file': ('django.db.models.fields.files.FileField', [], {'max_length': '1000', 'null': 'True', 'blank': 'True'}),
            u'id': ('django.db.models.fields.AutoField', [], {'primary_key': 'True'}),
            'media': ('django.db.models.fields.CharField', [], {'max_length': '36', 'null': 'True', 'blank': 'True'}),
            'mime_type': ('django.db.models.fields.CharField', [], {'max_length': '192', 'null': 'True', 'blank': 'True'}),
            'order': ('django.db.models.fields.IntegerField', [], {'null': 'True', 'blank': 'True'}),
            'participants': ('django.db.models.fields.related.ManyToManyField', [], {'symmetrical': 'False', 'to': u"orm['utils.Person']", 'null': 'True', 'through': u"orm['archives.Participant']", 'blank': 'True'}),
            'publisher': ('django.db.models.fields.related.ForeignKey', [], {'blank': 'True', 'related_name': "'publisher'", 'null': 'True', 'to': u"orm['utils.Collectivity']"}),
            'record_type': ('django.db.models.fields.CharField', [], {'max_length': '1', 'null': 'True', 'blank': 'True'}),
            'slideshow': ('django.db.models.fields.files.FileField', [], {'max_length': '100', 'null': 'True', 'blank': 'True'}),
            'slug': ('django.db.models.fields.SlugField', [], {'max_length': '50', 'unique': 'True', 'null': 'True', 'blank': 'True'}),
            'summary': ('django.db.models.fields.TextField', [], {'null': 'True', 'blank': 'True'}),
            'thumbnail': ('django.db.models.fields.files.ImageField', [], {'max_length': '100', 'null': 'True', 'blank': 'True'}),
            'time_stamp': ('django.db.models.fields.DateTimeField', [], {'auto_now': 'True', 'blank': 'True'}),
            'title': ('django.db.models.fields.CharField', [], {'max_length': '255', 'null': 'True', 'blank': 'True'}),
            'user': ('django.db.models.fields.related.ForeignKey', [], {'to': u"orm['auth.User']", 'null': 'True', 'blank': 'True'}),
            'work': ('django.db.models.fields.related.ForeignKey', [], {'to': u"orm['utils.Work']", 'null': 'True', 'blank': 'True'})
        },
        u'archives.mediacollectivity': {
            'Meta': {'unique_together': "(('media', 'collectivity'),)", 'object_name': 'MediaCollectivity', 'db_table': "'archives_media_collectivities'"},
            'collectivity': ('django.db.models.fields.related.ForeignKey', [], {'to': u"orm['utils.Collectivity']"}),
            u'id': ('django.db.models.fields.AutoField', [], {'primary_key': 'True'}),
            'media': ('django.db.models.fields.related.ForeignKey', [], {'to': u"orm['archives.Media']"}),
            'role': ('django.db.models.fields.related.ForeignKey', [], {'to': u"orm['utils.Role']", 'null': 'True', 'blank': 'True'}),
            'role_new': ('django.db.models.fields.related.ManyToManyField', [], {'blank': 'True', 'related_name': "'role_new4'", 'null': 'True', 'symmetrical': 'False', 'to': u"orm['utils.Role']"})
        },
        u'archives.orchestre': {
            'Meta': {'object_name': 'Orchestre', 'db_table': "u'orchestre'"},
            u'id': ('django.db.models.fields.AutoField', [], {'primary_key': 'True'}),
            'musiciens': ('django.db.models.fields.TextField', [], {'blank': 'True'}),
            'nom_chef': ('django.db.models.fields.CharField', [], {'max_length': "'255'", 'blank': 'True'}),
            'nom_complet': ('django.db.models.fields.CharField', [], {'max_length': "'255'", 'db_column': "'nom complet'", 'blank': 'True'}),
            'prenom_chef': ('django.db.models.fields.CharField', [], {'max_length': "'255'", 'blank': 'True'}),
            'role_chef': ('django.db.models.fields.CharField', [], {'max_length': "'255'", 'blank': 'True'}),
            'sous_titre': ('django.db.models.fields.TextField', [], {'db_column': "'sous titre'", 'blank': 'True'})
        },
        u'archives.participant': {
            'Meta': {'object_name': 'Participant'},
            u'id': ('django.db.models.fields.AutoField', [], {'primary_key': 'True'}),
            'media': ('django.db.models.fields.related.ForeignKey', [], {'to': u"orm['archives.Media']"}),
            'person': ('django.db.models.fields.related.ForeignKey', [], {'to': u"orm['utils.Person']"}),
            'role': ('django.db.models.fields.related.ForeignKey', [], {'to': u"orm['utils.Role']"}),
            'role_new': ('django.db.models.fields.related.ManyToManyField', [], {'blank': 'True', 'related_name': "'role_new2'", 'null': 'True', 'symmetrical': 'False', 'to': u"orm['utils.Role']"})
        },
        u'archives.set': {
            'Meta': {'ordering': "['label']", 'object_name': 'Set'},
            'comment': ('django.db.models.fields.CharField', [], {'max_length': '384', 'null': 'True', 'blank': 'True'}),
            u'id': ('django.db.models.fields.AutoField', [], {'primary_key': 'True'}),
            'label': ('django.db.models.fields.CharField', [], {'max_length': '255'}),
            'time_stamp': ('django.db.models.fields.DateTimeField', [], {'auto_now': 'True', 'blank': 'True'})
        },
        u'archives.shared': {
            'Meta': {'object_name': 'Shared'},
            'dailymotion': ('django.db.models.fields.CharField', [], {'max_length': '255', 'null': 'True', 'blank': 'True'}),
            u'id': ('django.db.models.fields.AutoField', [], {'primary_key': 'True'}),
            'media': ('django.db.models.fields.related.OneToOneField', [], {'to': u"orm['archives.Media']", 'unique': 'True'}),
            'soundcloud': ('django.db.models.fields.CharField', [], {'max_length': '255', 'null': 'True', 'blank': 'True'}),
            'vimeo': ('django.db.models.fields.CharField', [], {'max_length': '255', 'null': 'True', 'blank': 'True'}),
            'youtube': ('django.db.models.fields.CharField', [], {'max_length': '255', 'null': 'True', 'blank': 'True'})
        },
        u'archives.tag': {
            'Meta': {'object_name': 'Tag'},
            'comment': ('django.db.models.fields.TextField', [], {'null': 'True', 'blank': 'True'}),
            u'id': ('django.db.models.fields.AutoField', [], {'primary_key': 'True'}),
            'label': ('django.db.models.fields.CharField', [], {'max_length': '255'}),
            'time_stamp': ('django.db.models.fields.DateTimeField', [], {'auto_now': 'True', 'blank': 'True'})
        },
        u'auth.group': {
            'Meta': {'object_name': 'Group'},
            u'id': ('django.db.models.fields.AutoField', [], {'primary_key': 'True'}),
            'name': ('django.db.models.fields.CharField', [], {'unique': 'True', 'max_length': '80'}),
            'permissions': ('django.db.models.fields.related.ManyToManyField', [], {'to': u"orm['auth.Permission']", 'symmetrical': 'False', 'blank': 'True'})
        },
        u'auth.permission': {
            'Meta': {'ordering': "(u'content_type__app_label', u'content_type__model', u'codename')", 'unique_together': "((u'content_type', u'codename'),)", 'object_name': 'Permission'},
            'codename': ('django.db.models.fields.CharField', [], {'max_length': '100'}),
            'content_type': ('django.db.models.fields.related.ForeignKey', [], {'to': u"orm['contenttypes.ContentType']"}),
            u'id': ('django.db.models.fields.AutoField', [], {'primary_key': 'True'}),
            'name': ('django.db.models.fields.CharField', [], {'max_length': '50'})
        },
        u'auth.user': {
            'Meta': {'object_name': 'User'},
            'date_joined': ('django.db.models.fields.DateTimeField', [], {'default': 'datetime.datetime.now'}),
            'email': ('django.db.models.fields.EmailField', [], {'max_length': '75', 'blank': 'True'}),
            'first_name': ('django.db.models.fields.CharField', [], {'max_length': '30', 'blank': 'True'}),
            'groups': ('django.db.models.fields.related.ManyToManyField', [], {'to': u"orm['auth.Group']", 'symmetrical': 'False', 'blank': 'True'}),
            u'id': ('django.db.models.fields.AutoField', [], {'primary_key': 'True'}),
            'is_active': ('django.db.models.fields.BooleanField', [], {'default': 'True'}),
            'is_staff': ('django.db.models.fields.BooleanField', [], {'default': 'False'}),
            'is_superuser': ('django.db.models.fields.BooleanField', [], {'default': 'False'}),
            'last_login': ('django.db.models.fields.DateTimeField', [], {'default': 'datetime.datetime.now'}),
            'last_name': ('django.db.models.fields.CharField', [], {'max_length': '30', 'blank': 'True'}),
            'password': ('django.db.models.fields.CharField', [], {'max_length': '128'}),
            'user_permissions': ('django.db.models.fields.related.ManyToManyField', [], {'to': u"orm['auth.Permission']", 'symmetrical': 'False', 'blank': 'True'}),
            'username': ('django.db.models.fields.CharField', [], {'unique': 'True', 'max_length': '30'})
        },
        u'contenttypes.contenttype': {
            'Meta': {'ordering': "('name',)", 'unique_together': "(('app_label', 'model'),)", 'object_name': 'ContentType', 'db_table': "'django_content_type'"},
            'app_label': ('django.db.models.fields.CharField', [], {'max_length': '100'}),
            u'id': ('django.db.models.fields.AutoField', [], {'primary_key': 'True'}),
            'model': ('django.db.models.fields.CharField', [], {'max_length': '100'}),
            'name': ('django.db.models.fields.CharField', [], {'max_length': '100'})
        },
        u'events.event': {
            'Meta': {'ordering': "['tree_id', 'lft']", 'object_name': 'Event'},
            'date_end': ('django.db.models.fields.DateField', [], {'null': 'True', 'blank': 'True'}),
            'date_start': ('django.db.models.fields.DateField', [], {'null': 'True', 'blank': 'True'}),
            'event_type': ('django.db.models.fields.related.ForeignKey', [], {'to': u"orm['events.EventType']", 'null': 'True', 'blank': 'True'}),
            u'id': ('django.db.models.fields.AutoField', [], {'primary_key': 'True'}),
            'level': ('django.db.models.fields.PositiveIntegerField', [], {'db_index': 'True'}),
            'lft': ('django.db.models.fields.PositiveIntegerField', [], {'db_index': 'True'}),
            'parent': ('mptt.fields.TreeForeignKey', [], {'blank': 'True', 'related_name': "'children'", 'null': 'True', 'on_delete': 'models.SET_NULL', 'to': u"orm['events.Event']"}),
            'rght': ('django.db.models.fields.PositiveIntegerField', [], {'db_index': 'True'}),
            'subtitle': ('django.db.models.fields.CharField', [], {'max_length': '384', 'null': 'True', 'blank': 'True'}),
            'time_stamp': ('django.db.models.fields.DateTimeField', [], {'auto_now': 'True', 'blank': 'True'}),
            'title': ('django.db.models.fields.CharField', [], {'max_length': '255'}),
            'tree_id': ('django.db.models.fields.PositiveIntegerField', [], {'db_index': 'True'})
        },
        u'events.eventtype': {
            'Meta': {'object_name': 'EventType'},
            u'id': ('django.db.models.fields.AutoField', [], {'primary_key': 'True'}),
            'label': ('django.db.models.fields.CharField', [], {'max_length': '255'}),
            'level': ('django.db.models.fields.PositiveIntegerField', [], {'db_index': 'True'}),
            'lft': ('django.db.models.fields.PositiveIntegerField', [], {'db_index': 'True'}),
            'parent': ('mptt.fields.TreeForeignKey', [], {'blank': 'True', 'related_name': "'children'", 'null': 'True', 'to': u"orm['events.EventType']"}),
            'rght': ('django.db.models.fields.PositiveIntegerField', [], {'db_index': 'True'}),
            'tree_id': ('django.db.models.fields.PositiveIntegerField', [], {'db_index': 'True'})
        },
        u'utils.collectivity': {
            'Meta': {'ordering': "['name']", 'object_name': 'Collectivity'},
            'description': ('django.db.models.fields.TextField', [], {'null': 'True', 'blank': 'True'}),
            u'id': ('django.db.models.fields.AutoField', [], {'primary_key': 'True'}),
            'name': ('django.db.models.fields.CharField', [], {'max_length': '255'})
        },
        u'utils.composer': {
            'Meta': {'object_name': 'Composer'},
            u'id': ('django.db.models.fields.AutoField', [], {'primary_key': 'True'}),
            'person': ('django.db.models.fields.related.ForeignKey', [], {'to': u"orm['utils.Person']"}),
            'role': ('django.db.models.fields.related.ForeignKey', [], {'to': u"orm['utils.Role']"}),
            'work': ('django.db.models.fields.related.ForeignKey', [], {'to': u"orm['utils.Work']"})
        },
        u'utils.person': {
            'Meta': {'ordering': "['last_name']", 'object_name': 'Person'},
            'biography': ('django.db.models.fields.TextField', [], {'null': 'True', 'blank': 'True'}),
            'first_name': ('django.db.models.fields.CharField', [], {'max_length': '150', 'null': 'True', 'blank': 'True'}),
            u'id': ('django.db.models.fields.AutoField', [], {'primary_key': 'True'}),
            'last_name': ('django.db.models.fields.CharField', [], {'max_length': '150'})
        },
        u'utils.place': {
            'Meta': {'object_name': 'Place'},
            'city': ('django.db.models.fields.CharField', [], {'max_length': '765'}),
            'country': ('django.db.models.fields.CharField', [], {'max_length': '765'}),
            'hall': ('django.db.models.fields.CharField', [], {'max_length': '255', 'null': 'True', 'blank': 'True'}),
            u'id': ('django.db.models.fields.AutoField', [], {'primary_key': 'True'}),
            'name': ('django.db.models.fields.CharField', [], {'max_length': '255'})
        },
        u'utils.role': {
            'Meta': {'object_name': 'Role'},
            u'id': ('django.db.models.fields.AutoField', [], {'primary_key': 'True'}),
            'label': ('django.db.models.fields.CharField', [], {'max_length': '255'})
        },
        u'utils.work': {
            'Meta': {'object_name': 'Work'},
            'collectivities': ('django.db.models.fields.related.ManyToManyField', [], {'symmetrical': 'False', 'to': u"orm['utils.Collectivity']", 'null': 'True', 'blank': 'True'}),
            'composers': ('django.db.models.fields.related.ManyToManyField', [], {'symmetrical': 'False', 'to': u"orm['utils.Person']", 'null': 'True', 'through': u"orm['utils.Composer']", 'blank': 'True'}),
            u'id': ('django.db.models.fields.AutoField', [], {'primary_key': 'True'}),
            'subtitle': ('django.db.models.fields.CharField', [], {'max_length': '384', 'null': 'True', 'blank': 'True'}),
            'title': ('django.db.models.fields.CharField', [], {'max_length': '384'}),
            'year': ('django.db.models.fields.CharField', [], {'max_length': '12', 'null': 'True', 'blank': 'True'})
        }
    }

    complete_apps = ['archives']