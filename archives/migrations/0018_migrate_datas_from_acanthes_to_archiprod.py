# -*- coding: utf-8 -*-
import re
import subprocess
import datetime
from south.db import db
from south.v2 import DataMigration
from django.db import models
from archives.acanthes import *

from django.core.exceptions import MultipleObjectsReturned


class Migration(DataMigration):

    def forwards(self, orm):
        # Note: Remember to use orm['appname.ModelName'] rather than "from appname.models..."
        # Intervenant => Person

        init_date = datetime.date(1900,1,1)

        intervenants = Intervenant.objects.all()
        intervenant_person = {}  # used to hold id intervenant / id person to create the link after
        for intervenant in intervenants:
            p = orm['utils.Person'](first_name=intervenant.prenom,
                                    last_name=intervenant.nom,
                                    biography=u"%s \n%s \n%s" % (intervenant.biographie, intervenant.web_1, intervenant.web_2))
            p.save()
            intervenant_person[intervenant.id] = p
        lieux = Lieu.objects.all()
        lieu_place = {}
        for lieu in lieux:
            place = orm['utils.Place'](name=lieu.salle,
                                       hall=lieu.salle,
                                       country=lieu.placeterm,
                                       city=lieu.placeterm)
            place.save()
            lieu_place[lieu.id] = place

        orchestres = Orchestre.objects.all()
        orchestre_collectivite = {}
        for orchestre in orchestres:
            collectivity = orm['utils.Collectivity'](name=orchestre.nom_complet,
                                                     description=u"%s \n musiciens: %s \n chef: %s %s (%s) " % (orchestre.sous_titre, orchestre.musiciens, orchestre.nom_chef, orchestre.prenom_chef, orchestre.role_chef))
            collectivity.save()
            orchestre_collectivite[orchestre.id] = collectivity

        acanthes_set = orm['archives.Set'](label="Acanthes", comment="issue de la base Acanthes")
        acanthes_set.save()
        acanthes_events = {}
        for i in range(1977, 2014):
            acanthes_event = orm['events.Event'](title="Acanthes %s" % (i), level=0, lft=0, rght=0, tree_id=0)
            acanthes_event.save()
            acanthes_events[i] = acanthes_event

        audios = Audio.objects.all()

        user = orm['auth.User'].objects.get(username='de-gelis')



        for audio in audios:
            title = audio.subtitle
            if audio.kf_id_intervenant_principal:
                title = u"%s %s : %s" % (audio.kf_id_intervenant_principal.prenom, audio.kf_id_intervenant_principal.nom, title)
            genres = audio.genre.split(',')
            tags = []
            for genre in genres:
                #t, val = orm['archives.Tag'].objects.get_or_create(label=genre.strip())
                objects = orm['archives.Tag'].objects.filter(label=genre.strip())
                if len(objects) == 0:
                    t = orm['archives.Tag'].objects.create(label=genre.strip())
                else:
                    t = objects[0]
                tags.append(t)
            # Archive creation
            archive = orm['archives.Archive'](id_archiprod='ACANTHES', set=acanthes_set,
                                              title=title,
                                              user=user, old_id=audio.id,
                                              available='1', state='1', pending='0')
            if audio.annee != '':
                archive.event = acanthes_events[int(audio.annee)]

            try:
                if audio.kf_id_lieu:
                    archive.place = lieu_place[audio.kf_id_lieu.id]
            except:
                #print 'PAS DE LIEU'
                pass

            try:

                if audio.kf_id_orchestre is not None:
                    archive.collectivities.add(orchestre_collectivite[int(audio.kf_id_orchestre.id)])

            except:
                #print 'PAS d ORCHESTRE %s' % (audio.subtitle)
                pass

            if audio.date_enregistrement:
                # set date of an archive, adding date_enregistrement to 1 janv 1900
                date = init_date + datetime.timedelta(days=int(audio.date_enregistrement))
                archive.date = date

            archive.save()
            archive.tags.add(*tags)

            # participants
            participants = IntervenantAudio.objects.filter(audio=audio)
            for participant in participants:
                try:
                    objects = orm['utils.Role'].objects.filter(label=participant.role)
                    if len(objects) == 0:
                        role = orm['utils.Role'].objects.create(label=participant.role)
                    else:
                        role = objects[0]
                    ap = orm['archives.ArchiveParticipant'](archive=archive,
                                                            role=role,
                                                            person=intervenant_person[int(participant.intervenant.id)])
                    ap.save()
                except:
                    pass

            # audio ref
            if audio.genre.lower() == "oeuvre(s) musicale(s)":
                # here, we have got a work ref.
                # we need first to get the composer
                composer = None
                for i in audio.intervenantaudio_set.all():
                    if i.role == "compositeur":
                        try:
                            composer, created = orm['utils.Person'].objects.get_or_create(first_name=i.intervenant.prenom,
                                last_name=i.intervenant.nom, defaults={'biography': i.intervenant.biographie})
                        except MultipleObjectsReturned:
                            composer = orm['utils.Person'].objects.filter(first_name=i.intervenant.prenom, last_name=i.intervenant.nom)[0]
                            if composer.biography is None and i.intervenant.biographie is not None:
                                # I get acanthes biography, in case we haven't any bio in current archiprod person
                                composer.biography = i.intervenant.biographie
                                composer.save()
                work = orm['utils.Work'](title=audio.subtitle)
                work.save()
                # below, bad hack to get role 'compositeur'
                #role = orm['utils.Role'].objects.get(id=425)
                role = orm['utils.Role'].objects.get(label='compositeur')
                if composer:
                    comp = orm['utils.Composer'](work=work, person=composer, role=role)
                    comp.save()

            # Media creation
            media = orm['archives.Media'](media='ACANTHES', archive=archive, title=title, comments=audio.remarque, confidentiality='1', record_type='0', summary=audio.abstract, user=user)
            media.file = 'acanthes/%s' % audio.url_ecoute_intranet_adresse

            media.save()

            # Media duration
            process = subprocess.Popen(["ffmpeg", "-i", media.file.path], stdout=subprocess.PIPE, stderr=subprocess.STDOUT)
            stdout, stderr = process.communicate()
            try:
                pattern = re.compile(r'Duration: ([\w.-]+):([\w.-]+):([\w.-]+),')
                match = pattern.search(stdout)
                duration = "%s:%s:%s" % (match.group(1), match.group(2), match.group(3))
            except:
                duration = None
            media.duration = duration

            media.save()

            try:
                if audio.kf_id_orchestre is not None:
                    media.collectivities.add(orchestre_collectivite[int(audio.kf_id_orchestre.id)])

            except:
                #print 'PAS d ORCHESTRE'
                pass
            for participant in participants:
                objects = orm['utils.Role'].objects.filter(label=participant.role)
                if len(objects) == 0:
                    role = orm['utils.Role'].objects.create(label=participant.role)
                else:
                    role = objects[0]
                #role, boolean = orm['utils.Role'].objects.get_or_create(label=participant.role)
                try:
                    mp = orm['archives.Participant'](media=media,
                                                     role=role,
                                                     person=intervenant_person[int(participant.intervenant.id)])
                    mp.save()
                except:
                    #print 'erreur intervenant'
                    pass
            media.save()


    def backwards(self, orm):
        "Write your backwards methods here."
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
            'id': ('django.db.models.fields.AutoField', [], {'primary_key': 'True'}),
            'id_archiprod': ('django.db.models.fields.CharField', [], {'max_length': '12'}),
            'note2prog_id': ('django.db.models.fields.CharField', [], {'max_length': '30', 'null': 'True', 'blank': 'True'}),
            'old_id': ('django.db.models.fields.CharField', [], {'max_length': '384', 'null': 'True', 'blank': 'True'}),
            'order': ('django.db.models.fields.CharField', [], {'default': 'None', 'max_length': '12', 'null': 'True', 'blank': 'True'}),
            'participants': ('django.db.models.fields.related.ManyToManyField', [], {'symmetrical': 'False', 'to': "orm['utils.Person']", 'null': 'True', 'through': "orm['archives.ArchiveParticipant']", 'blank': 'True'}),
            'pending': ('django.db.models.fields.CharField', [], {'max_length': '1', 'null': 'True', 'blank': 'True'}),
            'place': ('django.db.models.fields.related.ForeignKey', [], {'to': "orm['utils.Place']", 'null': 'True', 'blank': 'True'}),
            'reviewer': ('django.db.models.fields.related.ForeignKey', [], {'blank': 'True', 'related_name': "'reviewer'", 'null': 'True', 'to': "orm['auth.User']"}),
            'set': ('django.db.models.fields.related.ForeignKey', [], {'to': "orm['archives.Set']", 'null': 'True', 'blank': 'True'}),
            'state': ('django.db.models.fields.CharField', [], {'max_length': '1', 'null': 'True', 'blank': 'True'}),
            'subtitle': ('django.db.models.fields.CharField', [], {'max_length': '384', 'null': 'True', 'blank': 'True'}),
            'summary': ('django.db.models.fields.TextField', [], {'null': 'True', 'blank': 'True'}),
            'tags': ('django.db.models.fields.related.ManyToManyField', [], {'symmetrical': 'False', 'to': "orm['archives.Tag']", 'null': 'True', 'blank': 'True'}),
            'time': ('django.db.models.fields.TimeField', [], {'null': 'True', 'blank': 'True'}),
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
        'archives.audio': {
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
            'id': ('django.db.models.fields.AutoField', [], {'primary_key': 'True'}),
            'intervenants': ('django.db.models.fields.related.ManyToManyField', [], {'related_name': "'intervenants_audio'", 'symmetrical': 'False', 'through': "orm['archives.IntervenantAudio']", 'to': "orm['archives.Intervenant']"}),
            'kf_id_intervenant_principal': ('django.db.models.fields.related.ForeignKey', [], {'to': "orm['archives.Intervenant']", 'null': 'True', 'db_column': "'kf_ID_intervenant_principal'", 'blank': 'True'}),
            'kf_id_langue_1': ('django.db.models.fields.related.ForeignKey', [], {'blank': 'True', 'related_name': "'langue_1'", 'null': 'True', 'db_column': "'kf_ID_langue_1'", 'to': "orm['archives.Langue']"}),
            'kf_id_langue_2': ('django.db.models.fields.related.ForeignKey', [], {'blank': 'True', 'related_name': "'langue_2'", 'null': 'True', 'db_column': "'kf_ID_langue_2'", 'to': "orm['archives.Langue']"}),
            'kf_id_langue_3': ('django.db.models.fields.related.ForeignKey', [], {'blank': 'True', 'related_name': "'langue_3'", 'null': 'True', 'db_column': "'kf_ID_langue_3'", 'to': "orm['archives.Langue']"}),
            'kf_id_lieu': ('django.db.models.fields.related.ForeignKey', [], {'to': "orm['archives.Lieu']", 'null': 'True', 'db_column': "'kf_ID_lieu'", 'blank': 'True'}),
            'kf_id_orchestre': ('django.db.models.fields.related.ForeignKey', [], {'to': "orm['archives.Orchestre']", 'null': 'True', 'db_column': "'kf_ID_orchestre'", 'blank': 'True'}),
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
        'archives.intervenant': {
            'Meta': {'object_name': 'Intervenant', 'db_table': "u'intervenant'"},
            'biographie': ('django.db.models.fields.TextField', [], {'blank': 'True'}),
            'horodatage_creation': ('django.db.models.fields.TextField', [], {'blank': 'True'}),
            'horodatage_modification': ('django.db.models.fields.TextField', [], {'blank': 'True'}),
            'id': ('django.db.models.fields.AutoField', [], {'primary_key': 'True'}),
            'nom': ('django.db.models.fields.CharField', [], {'max_length': '255', 'db_column': "'Nom'", 'blank': 'True'}),
            'prenom': ('django.db.models.fields.CharField', [], {'max_length': '255', 'db_column': "u'Pr\\xe9nom'", 'blank': 'True'}),
            'prenom_nom': ('django.db.models.fields.CharField', [], {'max_length': '255', 'blank': 'True'}),
            'web_1': ('django.db.models.fields.CharField', [], {'max_length': '255', 'blank': 'True'}),
            'web_2': ('django.db.models.fields.CharField', [], {'max_length': '255', 'blank': 'True'})
        },
        'archives.intervenantaudio': {
            'Meta': {'object_name': 'IntervenantAudio'},
            'audio': ('django.db.models.fields.related.ForeignKey', [], {'to': "orm['archives.Audio']"}),
            'id': ('django.db.models.fields.AutoField', [], {'primary_key': 'True'}),
            'intervenant': ('django.db.models.fields.related.ForeignKey', [], {'to': "orm['archives.Intervenant']"}),
            'ordre': ('django.db.models.fields.IntegerField', [], {'null': 'True', 'blank': 'True'}),
            'role': ('django.db.models.fields.CharField', [], {'max_length': '255', 'null': 'True', 'blank': 'True'})
        },
        'archives.langue': {
            'Meta': {'object_name': 'Langue', 'db_table': "u'langue'"},
            'id': ('django.db.models.fields.AutoField', [], {'primary_key': 'True'}),
            'languageterm': ('django.db.models.fields.CharField', [], {'max_length': '255', 'db_column': "'languageTerm'", 'blank': 'True'})
        },
        'archives.lieu': {
            'Meta': {'object_name': 'Lieu', 'db_table': "u'lieu'"},
            'id': ('django.db.models.fields.AutoField', [], {'primary_key': 'True'}),
            'placeterm': ('django.db.models.fields.CharField', [], {'max_length': "'255'", 'db_column': "'placeTerm'", 'blank': 'True'}),
            'salle': ('django.db.models.fields.CharField', [], {'max_length': "'255'", 'blank': 'True'})
        },
        'archives.media': {
            'Meta': {'object_name': 'Media'},
            'archive': ('django.db.models.fields.related.ForeignKey', [], {'to': "orm['archives.Archive']", 'null': 'True', 'blank': 'True'}),
            'collectivities': ('django.db.models.fields.related.ManyToManyField', [], {'symmetrical': 'False', 'to': "orm['utils.Collectivity']", 'null': 'True', 'blank': 'True'}),
            'comments': ('django.db.models.fields.TextField', [], {'null': 'True', 'blank': 'True'}),
            'confidentiality': ('django.db.models.fields.CharField', [], {'max_length': '1', 'null': 'True', 'blank': 'True'}),
            'duration': ('django.db.models.fields.TimeField', [], {'null': 'True', 'blank': 'True'}),
            'file': ('django.db.models.fields.files.FileField', [], {'max_length': '100', 'null': 'True', 'blank': 'True'}),
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
        'archives.orchestre': {
            'Meta': {'object_name': 'Orchestre', 'db_table': "u'orchestre'"},
            'id': ('django.db.models.fields.AutoField', [], {'primary_key': 'True'}),
            'musiciens': ('django.db.models.fields.TextField', [], {'blank': 'True'}),
            'nom_chef': ('django.db.models.fields.CharField', [], {'max_length': "'255'", 'blank': 'True'}),
            'nom_complet': ('django.db.models.fields.CharField', [], {'max_length': "'255'", 'db_column': "'nom complet'", 'blank': 'True'}),
            'prenom_chef': ('django.db.models.fields.CharField', [], {'max_length': "'255'", 'blank': 'True'}),
            'role_chef': ('django.db.models.fields.CharField', [], {'max_length': "'255'", 'blank': 'True'}),
            'sous_titre': ('django.db.models.fields.TextField', [], {'db_column': "'sous titre'", 'blank': 'True'})
        },
        'archives.participant': {
            'Meta': {'object_name': 'Participant'},
            'id': ('django.db.models.fields.AutoField', [], {'primary_key': 'True'}),
            'media': ('django.db.models.fields.related.ForeignKey', [], {'to': "orm['archives.Media']"}),
            'person': ('django.db.models.fields.related.ForeignKey', [], {'to': "orm['utils.Person']"}),
            'role': ('django.db.models.fields.related.ForeignKey', [], {'to': "orm['utils.Role']"})
        },
        'archives.set': {
            'Meta': {'ordering': "['label']", 'object_name': 'Set'},
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
            'Meta': {'ordering': "['name']", 'object_name': 'Collectivity'},
            'description': ('django.db.models.fields.TextField', [], {'null': 'True', 'blank': 'True'}),
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
            'Meta': {'ordering': "['last_name']", 'object_name': 'Person'},
            'biography': ('django.db.models.fields.TextField', [], {'null': 'True', 'blank': 'True'}),
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
