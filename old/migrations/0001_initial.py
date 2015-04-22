# -*- coding: utf-8 -*-
import datetime
from south.db import db
from south.v2 import SchemaMigration
from django.db import models


class Migration(SchemaMigration):

    def forwards(self, orm):
        # Adding model 'ViewComposRussesOeuvres'
        db.create_table(u'_view_compos_russes_oeuvres', (
            ('oeuvre_titre', self.gf('django.db.models.fields.CharField')(max_length=384)),
            ('oeuvre_sous_titre', self.gf('django.db.models.fields.CharField')(max_length=384)),
            ('compositeur', self.gf('django.db.models.fields.CharField')(max_length=306)),
            ('id', self.gf('django.db.models.fields.CharField')(max_length=36, primary_key=True)),
            ('date_debut', self.gf('django.db.models.fields.DateField')(null=True, blank=True)),
            ('date_fin', self.gf('django.db.models.fields.DateField')(null=True, blank=True)),
            ('titre_concat', self.gf('django.db.models.fields.CharField')(max_length=384, blank=True)),
        ))
        db.send_create_signal('old', ['ViewComposRussesOeuvres'])

        # Adding model 'ViewEvenementVolume'
        db.create_table(u'_view_evenement_volume', (
            ('volume_id', self.gf('django.db.models.fields.CharField')(max_length=36, primary_key=True)),
            ('titre_concat', self.gf('django.db.models.fields.CharField')(max_length=384, blank=True)),
            ('titre_simple', self.gf('django.db.models.fields.CharField')(max_length=765, blank=True)),
        ))
        db.send_create_signal('old', ['ViewEvenementVolume'])

        # Adding model 'Collectivite'
        db.create_table(u'collectivite', (
            ('id', self.gf('django.db.models.fields.IntegerField')(primary_key=True)),
            ('supprime', self.gf('django.db.models.fields.IntegerField')(unique=True)),
            ('nom', self.gf('django.db.models.fields.CharField')(unique=True, max_length=255)),
            ('indice', self.gf('django.db.models.fields.IntegerField')()),
            ('forme_canonique', self.gf('django.db.models.fields.IntegerField')()),
        ))
        db.send_create_signal('old', ['Collectivite'])

        # Adding model 'Contrat'
        db.create_table(u'contrat', (
            ('id', self.gf('django.db.models.fields.IntegerField')(primary_key=True)),
            ('supprime', self.gf('django.db.models.fields.IntegerField')(unique=True)),
            ('intitule', self.gf('django.db.models.fields.CharField')(unique=True, max_length=255)),
            ('type', self.gf('django.db.models.fields.IntegerField')()),
            ('parent', self.gf('django.db.models.fields.CharField')(max_length=48)),
            ('notes', self.gf('django.db.models.fields.TextField')()),
            ('num_pages', self.gf('django.db.models.fields.IntegerField')(null=True, blank=True)),
            ('technicien', self.gf('django.db.models.fields.IntegerField')()),
            ('mime_type', self.gf('django.db.models.fields.CharField')(max_length=765)),
            ('time_stamp', self.gf('django.db.models.fields.DateTimeField')()),
        ))
        db.send_create_signal('old', ['Contrat'])

        # Adding model 'Evenement'
        db.create_table(u'evenement', (
            ('id', self.gf('django.db.models.fields.IntegerField')(primary_key=True)),
            ('supprime', self.gf('django.db.models.fields.IntegerField')(unique=True)),
            ('intitule', self.gf('django.db.models.fields.CharField')(unique=True, max_length=255)),
            ('sous_titre', self.gf('django.db.models.fields.CharField')(max_length=384)),
            ('parent', self.gf('django.db.models.fields.IntegerField')()),
            ('type', self.gf('django.db.models.fields.IntegerField')()),
            ('date_debut', self.gf('django.db.models.fields.DateField')(null=True, blank=True)),
            ('date_fin', self.gf('django.db.models.fields.DateField')(null=True, blank=True)),
            ('time_stamp', self.gf('django.db.models.fields.DateTimeField')()),
            ('event_children', self.gf('django.db.models.fields.IntegerField')()),
            ('audio_children', self.gf('django.db.models.fields.IntegerField')()),
            ('pdf_children', self.gf('django.db.models.fields.IntegerField')()),
            ('video_children', self.gf('django.db.models.fields.IntegerField')()),
        ))
        db.send_create_signal('old', ['Evenement'])

        # Adding model 'Lieu'
        db.create_table(u'lieu', (
            ('id', self.gf('django.db.models.fields.IntegerField')(primary_key=True)),
            ('supprime', self.gf('django.db.models.fields.IntegerField')(unique=True)),
            ('nom', self.gf('django.db.models.fields.CharField')(unique=True, max_length=255)),
            ('salle', self.gf('django.db.models.fields.CharField')(unique=True, max_length=255)),
            ('pays', self.gf('django.db.models.fields.CharField')(max_length=765)),
            ('ville', self.gf('django.db.models.fields.CharField')(max_length=765)),
        ))
        db.send_create_signal('old', ['Lieu'])

        # Adding model 'NotePersonneRoleEdit'
        db.create_table(u'note_personne_role_edit', (
            ('id', self.gf('django.db.models.fields.IntegerField')(primary_key=True)),
            ('note_programme', self.gf('django.db.models.fields.IntegerField')()),
            ('personne', self.gf('django.db.models.fields.IntegerField')()),
            ('role', self.gf('django.db.models.fields.IntegerField')()),
        ))
        db.send_create_signal('old', ['NotePersonneRoleEdit'])

        # Adding model 'NoteProgramme'
        db.create_table(u'note_programme', (
            ('id', self.gf('django.db.models.fields.IntegerField')(primary_key=True)),
            ('id_loris', self.gf('django.db.models.fields.CharField')(unique=True, max_length=15)),
            ('supprime', self.gf('django.db.models.fields.IntegerField')(unique=True)),
            ('intitule', self.gf('django.db.models.fields.CharField')(unique=True, max_length=255)),
            ('notes', self.gf('django.db.models.fields.TextField')()),
            ('num_pages', self.gf('django.db.models.fields.IntegerField')(null=True, blank=True)),
            ('editeur', self.gf('django.db.models.fields.IntegerField')()),
            ('parent', self.gf('django.db.models.fields.IntegerField')()),
            ('type', self.gf('django.db.models.fields.IntegerField')()),
            ('date_transfert', self.gf('django.db.models.fields.DateField')(null=True, blank=True)),
            ('technicien', self.gf('django.db.models.fields.IntegerField')()),
            ('confidentialite', self.gf('django.db.models.fields.IntegerField')()),
            ('mime_type', self.gf('django.db.models.fields.CharField')(max_length=765)),
            ('time_stamp', self.gf('django.db.models.fields.DateTimeField')()),
            ('etat_note', self.gf('django.db.models.fields.IntegerField')()),
        ))
        db.send_create_signal('old', ['NoteProgramme'])

        # Adding model 'Oeuvre'
        db.create_table(u'oeuvre', (
            ('id', self.gf('django.db.models.fields.IntegerField')(primary_key=True)),
            ('supprime', self.gf('django.db.models.fields.IntegerField')(unique=True)),
            ('titre', self.gf('django.db.models.fields.CharField')(max_length=384)),
            ('sous_titre', self.gf('django.db.models.fields.CharField')(max_length=384)),
            ('annee', self.gf('django.db.models.fields.CharField')(unique=True, max_length=12)),
        ))
        db.send_create_signal('old', ['Oeuvre'])

        # Adding model 'OeuvrePersonneRole'
        db.create_table(u'oeuvre_personne_role', (
            ('id', self.gf('django.db.models.fields.IntegerField')(primary_key=True)),
            ('oeuvre', self.gf('django.db.models.fields.IntegerField')()),
            ('personne', self.gf('django.db.models.fields.IntegerField')()),
            ('role', self.gf('django.db.models.fields.IntegerField')()),
        ))
        db.send_create_signal('old', ['OeuvrePersonneRole'])

        # Adding model 'PartieCollectivite'
        db.create_table(u'partie_collectivite', (
            ('id', self.gf('django.db.models.fields.IntegerField')(primary_key=True)),
            ('partie', self.gf('django.db.models.fields.CharField')(max_length=45)),
            ('collectivite', self.gf('django.db.models.fields.IntegerField')()),
        ))
        db.send_create_signal('old', ['PartieCollectivite'])

        # Adding model 'PartiePersonneRole'
        db.create_table(u'partie_personne_role', (
            ('id', self.gf('django.db.models.fields.IntegerField')(primary_key=True)),
            ('partie', self.gf('django.db.models.fields.CharField')(max_length=45)),
            ('personne', self.gf('django.db.models.fields.IntegerField')()),
            ('role', self.gf('django.db.models.fields.IntegerField')()),
        ))
        db.send_create_signal('old', ['PartiePersonneRole'])

        # Adding model 'Personne'
        db.create_table(u'personne', (
            ('id', self.gf('django.db.models.fields.IntegerField')(primary_key=True)),
            ('supprime', self.gf('django.db.models.fields.IntegerField')()),
            ('prenom', self.gf('django.db.models.fields.CharField')(max_length=150)),
            ('nom', self.gf('django.db.models.fields.CharField')(max_length=150)),
            ('prenom_na', self.gf('django.db.models.fields.CharField')(max_length=150)),
            ('nom_na', self.gf('django.db.models.fields.CharField')(max_length=150)),
            ('fonction', self.gf('django.db.models.fields.CharField')(max_length=90)),
            ('doris_key', self.gf('django.db.models.fields.IntegerField')()),
            ('brahms_key', self.gf('django.db.models.fields.CharField')(max_length=27)),
            ('indice', self.gf('django.db.models.fields.IntegerField')()),
            ('forme_canonique', self.gf('django.db.models.fields.IntegerField')()),
        ))
        db.send_create_signal('old', ['Personne'])

        # Adding model 'Precalc'
        db.create_table(u'precalc', (
            ('auto_id', self.gf('django.db.models.fields.IntegerField')(primary_key=True)),
            ('orig_id', self.gf('django.db.models.fields.CharField')(max_length=48)),
            ('oai_id', self.gf('django.db.models.fields.CharField')(max_length=96)),
            ('type', self.gf('django.db.models.fields.CharField')(max_length=48)),
            ('dc_data', self.gf('django.db.models.fields.TextField')()),
            ('mods_data', self.gf('django.db.models.fields.TextField')()),
            ('creation_stamp', self.gf('django.db.models.fields.DateTimeField')()),
            ('supprime', self.gf('django.db.models.fields.IntegerField')()),
        ))
        db.send_create_signal('old', ['Precalc'])

        # Adding model 'Role'
        db.create_table(u'role', (
            ('id', self.gf('django.db.models.fields.IntegerField')(primary_key=True)),
            ('supprime', self.gf('django.db.models.fields.IntegerField')(unique=True)),
            ('intitule', self.gf('django.db.models.fields.CharField')(unique=True, max_length=255)),
            ('indice', self.gf('django.db.models.fields.IntegerField')()),
            ('forme_canonique', self.gf('django.db.models.fields.IntegerField')()),
        ))
        db.send_create_signal('old', ['Role'])

        # Adding model 'RoleEdit'
        db.create_table(u'role_edit', (
            ('id', self.gf('django.db.models.fields.IntegerField')(primary_key=True)),
            ('supprime', self.gf('django.db.models.fields.IntegerField')(unique=True)),
            ('intitule', self.gf('django.db.models.fields.CharField')(unique=True, max_length=255)),
            ('indice', self.gf('django.db.models.fields.IntegerField')()),
            ('forme_canonique', self.gf('django.db.models.fields.IntegerField')()),
        ))
        db.send_create_signal('old', ['RoleEdit'])

        # Adding model 'TestViewOaiRecords'
        db.create_table(u'test_view_oai_records', (
            ('id', self.gf('django.db.models.fields.CharField')(max_length=48, primary_key=True)),
            ('type_notice', self.gf('django.db.models.fields.BigIntegerField')()),
            ('titre', self.gf('django.db.models.fields.CharField')(max_length=765, blank=True)),
            ('type_event', self.gf('django.db.models.fields.CharField')(max_length=12, blank=True)),
            ('sous_titre', self.gf('django.db.models.fields.CharField')(max_length=384)),
            ('parent', self.gf('django.db.models.fields.IntegerField')()),
            ('supprime', self.gf('django.db.models.fields.IntegerField')()),
            ('oai_set', self.gf('django.db.models.fields.CharField')(max_length=21)),
            ('time_stamp', self.gf('django.db.models.fields.DateTimeField')()),
            ('date_debut', self.gf('django.db.models.fields.CharField')(max_length=30, blank=True)),
            ('date_fin', self.gf('django.db.models.fields.CharField')(max_length=30, blank=True)),
            ('place', self.gf('django.db.models.fields.CharField')(max_length=384)),
            ('titre_parent', self.gf('django.db.models.fields.CharField')(max_length=765, blank=True)),
            ('date_pub', self.gf('django.db.models.fields.CharField')(max_length=30, blank=True)),
            ('publisher', self.gf('django.db.models.fields.CharField')(max_length=765)),
            ('confidentialite', self.gf('django.db.models.fields.CharField')(max_length=33)),
            ('id_loris', self.gf('django.db.models.fields.CharField')(max_length=15)),
            ('debut_parent', self.gf('django.db.models.fields.DateField')(null=True, blank=True)),
            ('fin_parent', self.gf('django.db.models.fields.DateField')(null=True, blank=True)),
        ))
        db.send_create_signal('old', ['TestViewOaiRecords'])

        # Adding model 'TypeEvenement'
        db.create_table(u'type_evenement', (
            ('id', self.gf('django.db.models.fields.IntegerField')(primary_key=True)),
            ('supprime', self.gf('django.db.models.fields.IntegerField')(unique=True)),
            ('intitule', self.gf('django.db.models.fields.CharField')(unique=True, max_length=255)),
        ))
        db.send_create_signal('old', ['TypeEvenement'])

        # Adding model 'Utilisateur'
        db.create_table(u'utilisateur', (
            ('id', self.gf('django.db.models.fields.IntegerField')(primary_key=True)),
            ('supprime', self.gf('django.db.models.fields.IntegerField')()),
            ('nom', self.gf('django.db.models.fields.CharField')(unique=True, max_length=255)),
            ('alt_login', self.gf('django.db.models.fields.CharField')(max_length=384)),
            ('prenom', self.gf('django.db.models.fields.CharField')(unique=True, max_length=255)),
            ('droits', self.gf('django.db.models.fields.IntegerField')()),
        ))
        db.send_create_signal('old', ['Utilisateur'])

        # Adding model 'VideoRecord'
        db.create_table(u'video_record', (
            ('id', self.gf('django.db.models.fields.IntegerField')(primary_key=True)),
            ('intitule', self.gf('django.db.models.fields.TextField')()),
            ('type_record', self.gf('django.db.models.fields.IntegerField')()),
            ('duree', self.gf('django.db.models.fields.TextField')()),
            ('notes', self.gf('django.db.models.fields.TextField')(blank=True)),
            ('resume', self.gf('django.db.models.fields.TextField')()),
            ('temp_file_name', self.gf('django.db.models.fields.CharField')(max_length=384)),
            ('archived_file_name', self.gf('django.db.models.fields.CharField')(max_length=192)),
            ('time_stamp', self.gf('django.db.models.fields.DateTimeField')()),
            ('parent', self.gf('django.db.models.fields.CharField')(max_length=48)),
            ('type', self.gf('django.db.models.fields.IntegerField')(null=True, blank=True)),
            ('mime_type', self.gf('django.db.models.fields.CharField')(max_length=192)),
            ('date_transfert', self.gf('django.db.models.fields.DateField')(null=True, blank=True)),
            ('supprime', self.gf('django.db.models.fields.IntegerField')()),
            ('technicien', self.gf('django.db.models.fields.IntegerField')()),
            ('confidentialite_record', self.gf('django.db.models.fields.IntegerField')()),
            ('archived', self.gf('django.db.models.fields.IntegerField')()),
            ('online', self.gf('django.db.models.fields.IntegerField')()),
            ('old_x', self.gf('django.db.models.fields.IntegerField')()),
            ('old_y', self.gf('django.db.models.fields.IntegerField')()),
            ('new_x', self.gf('django.db.models.fields.IntegerField')()),
            ('new_y', self.gf('django.db.models.fields.IntegerField')()),
        ))
        db.send_create_signal('old', ['VideoRecord'])

        # Adding model 'VideoRecordCollectivite'
        db.create_table(u'video_record_collectivite', (
            ('id', self.gf('django.db.models.fields.IntegerField')(primary_key=True)),
            ('video_record', self.gf('django.db.models.fields.CharField')(max_length=30)),
            ('collectivite', self.gf('django.db.models.fields.IntegerField')()),
        ))
        db.send_create_signal('old', ['VideoRecordCollectivite'])

        # Adding model 'VideoRecordPersonneRole'
        db.create_table(u'video_record_personne_role', (
            ('id', self.gf('django.db.models.fields.IntegerField')(primary_key=True)),
            ('video_record', self.gf('django.db.models.fields.CharField')(max_length=30)),
            ('personne', self.gf('django.db.models.fields.IntegerField')()),
            ('role', self.gf('django.db.models.fields.IntegerField')()),
        ))
        db.send_create_signal('old', ['VideoRecordPersonneRole'])

        # Adding model 'VideoSet'
        db.create_table(u'video_set', (
            ('id', self.gf('django.db.models.fields.IntegerField')(primary_key=True)),
            ('supprime', self.gf('django.db.models.fields.IntegerField')(unique=True)),
            ('intitule', self.gf('django.db.models.fields.CharField')(unique=True, max_length=255)),
            ('sous_titre', self.gf('django.db.models.fields.CharField')(max_length=384)),
            ('parent', self.gf('django.db.models.fields.IntegerField')()),
            ('time_stamp', self.gf('django.db.models.fields.DateTimeField')()),
            ('date_debut', self.gf('django.db.models.fields.DateField')(null=True, blank=True)),
            ('date_fin', self.gf('django.db.models.fields.DateField')(null=True, blank=True)),
            ('notes', self.gf('django.db.models.fields.TextField')()),
            ('resume', self.gf('django.db.models.fields.TextField')()),
        ))
        db.send_create_signal('old', ['VideoSet'])

        # Adding model 'VideoVolume'
        db.create_table(u'video_volume', (
            ('id', self.gf('django.db.models.fields.CharField')(max_length=36, primary_key=True)),
            ('intitule', self.gf('django.db.models.fields.TextField')()),
            ('annee', self.gf('django.db.models.fields.TextField')(blank=True)),
            ('date', self.gf('django.db.models.fields.DateField')(null=True, blank=True)),
            ('notes', self.gf('django.db.models.fields.TextField')(blank=True)),
            ('resume', self.gf('django.db.models.fields.TextField')()),
            ('time_stamp', self.gf('django.db.models.fields.DateTimeField')()),
            ('parent', self.gf('django.db.models.fields.IntegerField')()),
            ('sort', self.gf('django.db.models.fields.CharField')(max_length=6)),
            ('type', self.gf('django.db.models.fields.IntegerField')(null=True, blank=True)),
            ('date_transfert', self.gf('django.db.models.fields.DateField')(null=True, blank=True)),
            ('supprime', self.gf('django.db.models.fields.IntegerField')()),
            ('technicien', self.gf('django.db.models.fields.IntegerField')()),
            ('lieu', self.gf('django.db.models.fields.IntegerField')()),
            ('horaire', self.gf('django.db.models.fields.CharField')(max_length=15)),
        ))
        db.send_create_signal('old', ['VideoVolume'])

        # Adding model 'VideoVolumeCollectivite'
        db.create_table(u'video_volume_collectivite', (
            ('id', self.gf('django.db.models.fields.IntegerField')(primary_key=True)),
            ('video_volume', self.gf('django.db.models.fields.CharField')(max_length=30)),
            ('collectivite', self.gf('django.db.models.fields.IntegerField')()),
        ))
        db.send_create_signal('old', ['VideoVolumeCollectivite'])

        # Adding model 'VideoVolumePersonneRole'
        db.create_table(u'video_volume_personne_role', (
            ('id', self.gf('django.db.models.fields.IntegerField')(primary_key=True)),
            ('video_volume', self.gf('django.db.models.fields.CharField')(max_length=30)),
            ('personne', self.gf('django.db.models.fields.IntegerField')()),
            ('role', self.gf('django.db.models.fields.IntegerField')()),
        ))
        db.send_create_signal('old', ['VideoVolumePersonneRole'])

        # Adding model 'ViewTitreOeuvrePersonneRole'
        db.create_table(u'view_titre_oeuvre_personne_role', (
            ('partie_id', self.gf('django.db.models.fields.CharField')(max_length=36, primary_key=True)),
            ('titre', self.gf('django.db.models.fields.CharField')(max_length=96, blank=True)),
            ('auteur_personne_id', self.gf('django.db.models.fields.IntegerField')(null=True, blank=True)),
            ('intervenant_personne_id', self.gf('django.db.models.fields.CharField')(max_length=16, blank=True)),
            ('intervenant_role_id', self.gf('django.db.models.fields.CharField')(max_length=16, blank=True)),
            ('collectivite_id', self.gf('django.db.models.fields.IntegerField')(null=True, blank=True)),
        ))
        db.send_create_signal('old', ['ViewTitreOeuvrePersonneRole'])

        # Adding model 'Volume'
        db.create_table(u'volume', (
            ('id', self.gf('django.db.models.fields.CharField')(max_length=36, primary_key=True)),
            ('old_id', self.gf('django.db.models.fields.CharField')(max_length=384)),
            ('voltype', self.gf('django.db.models.fields.IntegerField')()),
            ('auteur', self.gf('django.db.models.fields.TextField')(blank=True)),
            ('intitule', self.gf('django.db.models.fields.TextField')()),
            ('intitule_na', self.gf('django.db.models.fields.TextField')()),
            ('label', self.gf('django.db.models.fields.TextField')(blank=True)),
            ('annee', self.gf('django.db.models.fields.TextField')(blank=True)),
            ('date', self.gf('django.db.models.fields.DateField')(null=True, blank=True)),
            ('notes', self.gf('django.db.models.fields.TextField')(blank=True)),
            ('resume', self.gf('django.db.models.fields.TextField')()),
            ('notes_na', self.gf('django.db.models.fields.TextField')(blank=True)),
            ('url', self.gf('django.db.models.fields.TextField')(blank=True)),
            ('doris_key', self.gf('django.db.models.fields.IntegerField')()),
            ('cddb', self.gf('django.db.models.fields.CharField')(max_length=24, db_column='CDDB', blank=True)),
            ('note2prog_id', self.gf('django.db.models.fields.CharField')(max_length=30)),
            ('time_stamp', self.gf('django.db.models.fields.DateTimeField')()),
            ('parent', self.gf('django.db.models.fields.related.ForeignKey')(to=orm['old.Evenement'])),
            ('date_transfert', self.gf('django.db.models.fields.DateField')(null=True, blank=True)),
            ('pret', self.gf('django.db.models.fields.IntegerField')()),
            ('supprime', self.gf('django.db.models.fields.IntegerField')()),
            ('technicien', self.gf('django.db.models.fields.related.ForeignKey')(to=orm['old.Utilisateur'])),
            ('lieu', self.gf('django.db.models.fields.IntegerField')()),
            ('horaire', self.gf('django.db.models.fields.CharField')(max_length=15)),
            ('etat_collection', self.gf('django.db.models.fields.IntegerField')()),
            ('etat_archive', self.gf('django.db.models.fields.IntegerField')()),
            ('confidentialite_volume', self.gf('django.db.models.fields.IntegerField')()),
            ('pending', self.gf('django.db.models.fields.IntegerField')()),
        ))
        db.send_create_signal('old', ['Volume'])

        # Adding model 'Partie'
        db.create_table(u'partie', (
            ('id', self.gf('django.db.models.fields.CharField')(max_length=36, primary_key=True)),
            ('seq', self.gf('django.db.models.fields.IntegerField')()),
            ('partype', self.gf('django.db.models.fields.IntegerField')()),
            ('auteur1', self.gf('django.db.models.fields.IntegerField')(null=True, blank=True)),
            ('auteur2', self.gf('django.db.models.fields.IntegerField')(null=True, blank=True)),
            ('auteur3', self.gf('django.db.models.fields.IntegerField')(null=True, blank=True)),
            ('auteur4', self.gf('django.db.models.fields.IntegerField')(null=True, blank=True)),
            ('titre', self.gf('django.db.models.fields.TextField')()),
            ('titre_na', self.gf('django.db.models.fields.TextField')()),
            ('duree', self.gf('django.db.models.fields.TextField')(blank=True)),
            ('resume', self.gf('django.db.models.fields.TextField')()),
            ('notes', self.gf('django.db.models.fields.CharField')(max_length=765)),
            ('doris_key', self.gf('django.db.models.fields.IntegerField')()),
            ('brahms_key', self.gf('django.db.models.fields.CharField')(max_length=27)),
            ('resume_na', self.gf('django.db.models.fields.TextField')()),
            ('time_stamp', self.gf('django.db.models.fields.DateTimeField')()),
            ('oeuvre', self.gf('django.db.models.fields.IntegerField')()),
            ('editeur_partition', self.gf('django.db.models.fields.IntegerField')()),
            ('confidentialite_partie', self.gf('django.db.models.fields.IntegerField')()),
            ('supprime', self.gf('django.db.models.fields.IntegerField')()),
        ))
        db.send_create_signal('old', ['Partie'])

        # Adding model 'VolumeCollectivite'
        db.create_table(u'volume_collectivite', (
            ('id', self.gf('django.db.models.fields.IntegerField')(primary_key=True)),
            ('volume', self.gf('django.db.models.fields.CharField')(max_length=30)),
            ('collectivite', self.gf('django.db.models.fields.IntegerField')()),
        ))
        db.send_create_signal('old', ['VolumeCollectivite'])

        # Adding model 'VolumePersonneRole'
        db.create_table(u'volume_personne_role', (
            ('id', self.gf('django.db.models.fields.IntegerField')(primary_key=True)),
            ('volume', self.gf('django.db.models.fields.CharField')(max_length=30)),
            ('personne', self.gf('django.db.models.fields.IntegerField')()),
            ('role', self.gf('django.db.models.fields.IntegerField')()),
        ))
        db.send_create_signal('old', ['VolumePersonneRole'])


    def backwards(self, orm):
        # Deleting model 'ViewComposRussesOeuvres'
        db.delete_table(u'_view_compos_russes_oeuvres')

        # Deleting model 'ViewEvenementVolume'
        db.delete_table(u'_view_evenement_volume')

        # Deleting model 'Collectivite'
        db.delete_table(u'collectivite')

        # Deleting model 'Contrat'
        db.delete_table(u'contrat')

        # Deleting model 'Evenement'
        db.delete_table(u'evenement')

        # Deleting model 'Lieu'
        db.delete_table(u'lieu')

        # Deleting model 'NotePersonneRoleEdit'
        db.delete_table(u'note_personne_role_edit')

        # Deleting model 'NoteProgramme'
        db.delete_table(u'note_programme')

        # Deleting model 'Oeuvre'
        db.delete_table(u'oeuvre')

        # Deleting model 'OeuvrePersonneRole'
        db.delete_table(u'oeuvre_personne_role')

        # Deleting model 'PartieCollectivite'
        db.delete_table(u'partie_collectivite')

        # Deleting model 'PartiePersonneRole'
        db.delete_table(u'partie_personne_role')

        # Deleting model 'Personne'
        db.delete_table(u'personne')

        # Deleting model 'Precalc'
        db.delete_table(u'precalc')

        # Deleting model 'Role'
        db.delete_table(u'role')

        # Deleting model 'RoleEdit'
        db.delete_table(u'role_edit')

        # Deleting model 'TestViewOaiRecords'
        db.delete_table(u'test_view_oai_records')

        # Deleting model 'TypeEvenement'
        db.delete_table(u'type_evenement')

        # Deleting model 'Utilisateur'
        db.delete_table(u'utilisateur')

        # Deleting model 'VideoRecord'
        db.delete_table(u'video_record')

        # Deleting model 'VideoRecordCollectivite'
        db.delete_table(u'video_record_collectivite')

        # Deleting model 'VideoRecordPersonneRole'
        db.delete_table(u'video_record_personne_role')

        # Deleting model 'VideoSet'
        db.delete_table(u'video_set')

        # Deleting model 'VideoVolume'
        db.delete_table(u'video_volume')

        # Deleting model 'VideoVolumeCollectivite'
        db.delete_table(u'video_volume_collectivite')

        # Deleting model 'VideoVolumePersonneRole'
        db.delete_table(u'video_volume_personne_role')

        # Deleting model 'ViewTitreOeuvrePersonneRole'
        db.delete_table(u'view_titre_oeuvre_personne_role')

        # Deleting model 'Volume'
        db.delete_table(u'volume')

        # Deleting model 'Partie'
        db.delete_table(u'partie')

        # Deleting model 'VolumeCollectivite'
        db.delete_table(u'volume_collectivite')

        # Deleting model 'VolumePersonneRole'
        db.delete_table(u'volume_personne_role')


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
            'Meta': {'object_name': 'Partie', 'db_table': "u'partie'"},
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
            'oeuvre': ('django.db.models.fields.IntegerField', [], {}),
            'partype': ('django.db.models.fields.IntegerField', [], {}),
            'resume': ('django.db.models.fields.TextField', [], {}),
            'resume_na': ('django.db.models.fields.TextField', [], {}),
            'seq': ('django.db.models.fields.IntegerField', [], {}),
            'supprime': ('django.db.models.fields.IntegerField', [], {}),
            'time_stamp': ('django.db.models.fields.DateTimeField', [], {}),
            'titre': ('django.db.models.fields.TextField', [], {}),
            'titre_na': ('django.db.models.fields.TextField', [], {})
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
            'collectivite': ('django.db.models.fields.IntegerField', [], {}),
            'id': ('django.db.models.fields.IntegerField', [], {'primary_key': 'True'}),
            'volume': ('django.db.models.fields.CharField', [], {'max_length': '30'})
        },
        'old.volumepersonnerole': {
            'Meta': {'object_name': 'VolumePersonneRole', 'db_table': "u'volume_personne_role'"},
            'id': ('django.db.models.fields.IntegerField', [], {'primary_key': 'True'}),
            'personne': ('django.db.models.fields.IntegerField', [], {}),
            'role': ('django.db.models.fields.IntegerField', [], {}),
            'volume': ('django.db.models.fields.CharField', [], {'max_length': '30'})
        }
    }

    complete_apps = ['old']