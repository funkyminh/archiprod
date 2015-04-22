# -*- coding: utf-8 -*-
from django.db import models
from mptt.models import MPTTModel, TreeForeignKey
from django.contrib.auth.models import User


class TagEvenement(models.Model):
    '''
    TagEvenement model

    * MD : used for new archiprod
    '''
    id = models.IntegerField(primary_key=True)
    intitule = models.CharField(max_length=255)
    sous_titre = models.CharField(max_length=384, null=True, blank=True)
    date_debut = models.DateField(null=True, blank=True)
    date_fin = models.DateField(null=True, blank=True)
    time_stamp = models.DateTimeField(auto_now=True)

    class Meta:
        db_table = u'tag_evenement'


class Saison(models.Model):
    '''
    Saison model

    * MD : used for new archiprod
    '''
    id = models.IntegerField(primary_key=True)
    intitule = models.CharField(max_length=255, unique=True)
    sous_titre = models.CharField(max_length=384, null=True, blank=True)
    date_debut = models.DateField(null=True, blank=True)
    date_fin = models.DateField(null=True, blank=True)
    time_stamp = models.DateTimeField(auto_now=True)

    class Meta:
        db_table = u'saison'


class TypeEvenement(models.Model):
    '''
    TypeEvenement model

    * datamodel review by sam
    * 0 unused/inconsistant field
    * MD : OK
    '''
    id = models.IntegerField(primary_key=True)
    # supprime = models.IntegerField(default=0)
    intitule = models.CharField(max_length=255, unique=True)

    def __unicode__(self):
        return self.intitule

    class Meta:
        db_table = u'type_evenement'


class Utilisateur(models.Model):
    '''
    Utilisateur model

    * datamodel review by sam
    * but model needs to be replaced by User
    '''
    id = models.IntegerField(primary_key=True)
    # supprime = models.IntegerField(default=0)
    nom = models.CharField(max_length=255)
    alt_login = models.CharField(max_length=384, null=True, blank=True)
    prenom = models.CharField(max_length=255)
    droits = models.IntegerField()

    def __unicode__(self):
        return self.nom

    class Meta:
        db_table = u'utilisateur'


class Personne(models.Model):
    '''
    Personne model

    * datamodel review by sam
    * 5 possible inconsistant/unused fields
    * indice field may be unnecessary
    * MD ACTION DONE : DELETE COLUMN indice et forme_canonique ??? --> pour le moment unused fiels
    '''
    INDICE_CHOICES = (
        ('-1', '-1 ?, visiblement : existe forme canonique et c forme rejetée ici'),
        ('0', '0 - ca veut dire quoi ce champ indice ?'),
        ('1', '1 ? visiblement : forme dite acceptée'),
    )

    id = models.IntegerField(primary_key=True)
    # supprime = models.IntegerField()
    prenom = models.CharField(max_length=150)
    nom = models.CharField(max_length=150)

    # unused/inconsistant fiels
    #fonction = models.CharField(max_length=90)  # tjrs vide
    #brahms_key = models.CharField(max_length=27, null=True, blank=True)  # pointe vers un très vieil ID
    #doris_key = models.IntegerField(null=True, blank=True)  # il me semble inutilisé : cf. Sandra
    #indice = models.CharField(max_length=2, choices=INDICE_CHOICES)  # ??? a quoi ça sert
    #forme_canonique = models.ForeignKey('self', null=True, blank=True)

    def __unicode__(self):
        return "%s %s" % (self.nom, self.prenom)

    class Meta:
        db_table = u'personne'


class Role(models.Model):
    '''
    Role model

    * datamodel review by sam
    * indice field may be unnecessary
    * MD ACTION DONE : DELETE COLUMN indice et forme_canonique ??? --> pour le moment unused fiels
    '''
    INDICE_CHOICES = (
        ('-1', '-1 ?, visiblement : existe forme canonique et c forme rejetée ici'),
        ('0', '0 - ca veut dire quoi ce champ indice ?'), #0 = forme rejetée
        ('1', '1 ? visiblement : forme dite acceptée'),
    )
    id = models.IntegerField(primary_key=True)
    # supprime = models.IntegerField(default=0)
    intitule = models.CharField(max_length=255, unique=True)

    #unused fields
    #indice = models.CharField(max_length=2, choices=INDICE_CHOICES)  # ??? a quoi ça sert
    #forme_canonique = models.ForeignKey('self', null=True, blank=True)

    def __unicode__(self):
        return self.intitule

    class Meta:
        db_table = u'role'


class Collectivite(models.Model):
    '''
    Collectivite model

    * datamodel review by sam
    * indice field may be unnecessary
    * MD ACTION DONE : DELETE COLUMN indice et forme_canonique ??? --> pour le moment unused fiels
    '''
    INDICE_CHOICES = (
        ('-1', '-1 ?, visiblement : existe forme canonique et c forme rejetée ici'),
        ('0', '0 - ca veut dire quoi ce champ indice ?'),
        ('1', '1 ? visiblement : forme dite acceptée'),
    )
    id = models.IntegerField(primary_key=True)
    # supprime = models.IntegerField(default=0)
    nom = models.CharField(max_length=255, unique=True)

    #unused fields
    #indice = models.CharField(max_length=2, choices=INDICE_CHOICES)
    #forme_canonique = models.ForeignKey('self', null=True, blank=True)

    def __unicode__(self):
        return self.nom

    class Meta:
        db_table = u'collectivite'


class Evenement(MPTTModel):
    '''
    Evenement model

    * datamodel review by sam
    * 4 possible inconsistant/unused fields
    * MD ACTION DONE : sous titre (vide --> NULL)s
    * MD ACTION DONE : parent_id (0 --> NULL)
    '''
    id = models.IntegerField(primary_key=True)
    # supprime = models.IntegerField(default=0)
    intitule = models.CharField(max_length=255, unique=True)
    sous_titre = models.CharField(max_length=384, null=True, blank=True)
    parent = TreeForeignKey('self', null=True, blank=True, related_name='children')
    #type = models.ForeignKey(TypeEvenement, null=True, blank=True)
    type_evenement = models.ForeignKey(TypeEvenement, null=True, blank=True)
    date_debut = models.DateField(null=True, blank=True)
    date_fin = models.DateField(null=True, blank=True)
    time_stamp = models.DateTimeField(auto_now=True)

    # unused
    #event_children = models.IntegerField(null=True, blank=True)
    #audio_children = models.IntegerField(null=True, blank=True)
    #pdf_children = models.IntegerField(null=True, blank=True)
    #video_children = models.IntegerField(null=True, blank=True)

    #fields for new archiprod evenement = CATEGORIE
    notes = models.TextField(null=True, blank=True)
    resume = models.TextField(null=True, blank=True)

    #temp for new archiprod
    #flag_archive = models.BooleanField()
    #flag_categorie = models.BooleanField()

    def __unicode__(self):
        return self.intitule

    class Meta:
        db_table = u'evenement'

    class MPTTMeta:
        order_insertion_by = ['intitule']


class Evenement2(MPTTModel):

    id = models.IntegerField(primary_key=True)
    # supprime = models.IntegerField(default=0)
    intitule = models.CharField(max_length=255)
    sous_titre = models.CharField(max_length=384, null=True, blank=True)
    #parent = models.IntegerField()
    #type_evenement = models.IntegerField()
    parent = TreeForeignKey('self', null=True, blank=True, related_name='children')
    type_evenement = models.ForeignKey(TypeEvenement, null=True, blank=True)
    date_debut = models.DateField(null=True, blank=True)
    date_fin = models.DateField(null=True, blank=True)
    time_stamp = models.DateTimeField(auto_now=True)
    #notes = models.TextField(null=True, blank=True)
    #resume = models.TextField(null=True, blank=True)
    flag_archive = models.BooleanField()
    flag_categorie = models.BooleanField()

    def __unicode__(self):
        return self.intitule

    class Meta:
        db_table = u'evenement2'

    class MPTTMeta:
        order_insertion_by = ['intitule']


class Lieu(models.Model):
    '''
    Lieu model

    * datamodel review by sam
    * 0 inconsistant/unused fields
    * MD ACTION DONE : salle (vide --> NULL)
    '''
    id = models.IntegerField(primary_key=True)
    # supprime = models.IntegerField(default=0)
    nom = models.CharField(max_length=255, unique=True)
    salle = models.CharField(max_length=255, null=True, blank=True)
    pays = models.CharField(max_length=765)
    ville = models.CharField(max_length=765)

    def __unicode__(self):
        return self.nom

    class Meta:
        db_table = u'lieu'


class NotePersonneRoleEdit(models.Model):
    '''
    NotePersonneRoleEdit model

    * datamodel review by sam
    * 0 inconsistant/unused fields
    * MD QUESTION : TABLE vide ?? CF Sandra pourquoi toujours vide
    '''
    id = models.IntegerField(primary_key=True)
    note_programme = models.IntegerField()
    personne = models.ForeignKey(Personne)
    role = models.ForeignKey(Role)

    class Meta:
        db_table = u'note_personne_role_edit'


class NoteProgramme(models.Model):
    """
    NoteProgramme class

    Used to describe a collection of audio, named 'Partie' (!)
    * datamodel review by sam
    * REVOIR UNUSED FIELDS
    * MD ACTION DONE : editeur (0 --> NULL)
    * MD ACTION DONE : notes/mime_type (vide --> NULL)
    * MD ACTION DONE : unused type toujours à 0 ? probablement unused field
    """
    CONFIDENTIALITE_CHOICES = (
        ('0', 'Non'),
        ('1', 'Oui / jamais utilisé dans archiprod actuel'),
    )
    ETAT_NOTE_CHOICES = (
        ('0', '0 - ca veut dire quoi ?'),
        ('1', '1 - ca veut dire quoi ?'),
    )
    id = models.IntegerField(primary_key=True)
    id_loris = models.CharField(max_length=15, unique=True)
    # supprime = models.IntegerField(default=0)
    intitule = models.CharField(max_length=255)
    notes = models.TextField(null=True, blank=True)
    num_pages = models.IntegerField(null=True, blank=True)
    editeur = models.ForeignKey(Collectivite, null=True, blank=True)
    parent = models.ForeignKey(Evenement)
    date_transfert = models.DateField(null=True, blank=True)
    technicien = models.ForeignKey(User)
    confidentialite = models.CharField(max_length=1, choices=CONFIDENTIALITE_CHOICES)
    mime_type = models.CharField(max_length=765, null=True, blank=True)
    time_stamp = models.DateTimeField(auto_now=True)
    etat_note = models.CharField(max_length=1, choices=ETAT_NOTE_CHOICES)  # a quoi sert ce champ
    program = models.FileField(upload_to="programs", null=True, blank=True)
    program_ext = models.FileField(upload_to="programs/ext", null=True, blank=True)
    program_int = models.FileField(upload_to="programs/int", null=True, blank=True)

    # unused fields
    #type = models.ForeignKey(TypeEvenement, null=True, blank=True)

    #for new archiprod
    sous_titre = models.CharField(max_length=384, null=True, blank=True)
    tag_evenements = models.ManyToManyField(TagEvenement, null=True, blank=True)
    type_evenement = models.ForeignKey(TypeEvenement, null=True, blank=True)
    saison = models.ForeignKey(Saison, null=True, blank=True)

    # for new schema
    evenement2 = models.ForeignKey(Evenement2, null=True, blank=True)

    def __unicode__(self):
        return self.intitule

    class Meta:
        db_table = u'note_programme'


class Oeuvre(models.Model):
    '''
    Oeuvre model

    * datamodel review by sam
    * 0 inconsistant/unused fields
    * MD : OK
    '''
    id = models.IntegerField(primary_key=True)
    # supprime = models.IntegerField(default=0)
    titre = models.CharField(max_length=384)
    sous_titre = models.CharField(max_length=384, null=True, blank=True)
    annee = models.CharField(max_length=12, null=True, blank=True)  # il a des données de ce champs qui valent '????', à remplacer.

    def __unicode__(self):
        return self.titre

    class Meta:
        db_table = u'oeuvre'


class OeuvrePersonneRole(models.Model):
    '''
    OeuvrePersonneRole model

    * datamodel review by sam
    * 0 inconsistant/unused fields
    * MD : OK
    '''
    id = models.IntegerField(primary_key=True)
    oeuvre = models.ForeignKey(Oeuvre)
    personne = models.ForeignKey(Personne)
    role = models.ForeignKey(Role)

    class Meta:
        db_table = u'oeuvre_personne_role'


class VideoVolume(models.Model):
    '''
    VideoVolume model

    * datamodel review by sam
    * 0 inconsistant/unused fields
    * MD ACTION DONE : intitulé/notes/resume (vide--> NULL)
    * MS ACTION DONE : parent (0 --> NULL)
    * MD ACTION DONE : date passer 0000-00-00 à NULL
    '''
    TYPE_CHOICES = (
        ('1', 'Arbre des evenements'),
        ('2', 'Arbre des series documentaires'),
    )
    id = models.CharField(max_length=12, primary_key=True)
    intitule = models.TextField(null=True, blank=True)
    #rempli lorsque type=2
    #sinon vide lorsque type=1 et intitule video_volume provient de intitule évènement
    date = models.DateField(null=True, blank=True)
    notes = models.TextField(blank=True)
    resume = models.TextField(null=True, blank=True)
    time_stamp = models.DateTimeField(auto_now=True)  # on update CURRENT_TIMESTAMP
    parent = models.ForeignKey(Evenement, null=True, blank=True)  # passer parent=0 à parent=NULL
    sort = models.CharField(max_length=12, default=None, null=True, blank=True)
    type = models.CharField(max_length=1, choices=TYPE_CHOICES, null=True, blank=True)
    #type=NULL videos supprimées, doublon avec champ supprime=1
    # supprime = models.IntegerField(default=0)  # mettre à 1 pour action delete
    #à masquer du formulaire d'admin
    #mettre à 0 lorsqu'on sauve
    #mettre à 1 lorsque'on supprime
    technicien = models.ForeignKey(User, null=True, blank=True)
    lieu = models.ForeignKey(Lieu, null=True, blank=True)
    horaire = models.CharField(max_length=5,  default=None, null=True, blank=True)  # horaire de l'évènement vidéo

    #for new archiprod
    sous_titre = models.CharField(max_length=384, null=True, blank=True)
    #tag_evenement = models.ForeignKey(TagEvenement, null=True, blank=True)
    tag_evenements = models.ManyToManyField(TagEvenement, null=True, blank=True)
    type_evenement = models.ForeignKey(TypeEvenement, null=True, blank=True)
    saison = models.ForeignKey(Saison, null=True, blank=True)

    # for new schema
    evenement2 = models.ForeignKey(Evenement2, null=True, blank=True)

    def __unicode__(self):
        return self.id

    class Meta:
        db_table = u'video_volume'


class Contrat(models.Model):
    '''
    Contrat model

    * datamodel review by sam
    * 0 inconsistant/unused fields
    * MD ACTION DONE : notes (vide --> NULL)
    * MD ACTION DONE : mime_type à supprimer ? garder pour le moment (probablement unused)
    '''
    TYPE_CHOICES = (
        ('2', 'Type de type 2 ! a quoi cela sert'),
    )
    id = models.IntegerField(primary_key=True)
    # supprime = models.IntegerField(default=0)
    intitule = models.CharField(max_length=255)
    type = models.CharField(max_length=1, choices=TYPE_CHOICES)
    parent = models.ForeignKey(VideoVolume)
    notes = models.TextField(null=True, blank=True)
    num_pages = models.IntegerField(null=True, blank=True)
    technicien = models.ForeignKey(User)
    time_stamp = models.DateTimeField(auto_now=True)
    contract = models.FileField(upload_to="contracts", null=True, blank=True)

    #unused
    #mime_type = models.CharField(max_length=765, null=True, blank=True)  # jamais renseigné !

    def __unicode__(self):
        return self.intitule

    class Meta:
        db_table = u'contrat'


class VideoVolumeCollectivite(models.Model):
    '''
    VideoVolumeCollectivite model

    * datamodel review by sam
    * 0 inconsistant/unused fields
    * MD : OK
    '''
    id = models.IntegerField(primary_key=True)
    video_volume = models.ForeignKey(VideoVolume)
    collectivite = models.ForeignKey(Collectivite)

    class Meta:
        db_table = u'video_volume_collectivite'


class VideoVolumePersonneRole(models.Model):
    '''
    VideoVolumePersonneRole model

    * datamodel review by sam
    * 0 inconsistant/unused fields
    * MD : OK
    '''
    id = models.IntegerField(primary_key=True)
    video_volume = models.ForeignKey(VideoVolume)
    personne = models.ForeignKey(Personne)
    role = models.ForeignKey(Role)

    class Meta:
        db_table = u'video_volume_personne_role'


class VideoRecord(models.Model):
    '''
    VideoRecord model

    * datamodel review by sam
    * 9 inconsistant/unused fields
    * MD ACTION DONE : notes/resume (vide --> NULL)
    '''
    TYPE_RECORD_CHOICES = (
        ('0', 'Production'),
        ('1', 'Bonus'),
        ('2', 'Rush'),
    )
    CONFIDENTIALITE_RECORD_CHOICES = (
        ('0', 'Interne - Externe'),
        ('1', 'Interne'),
    )
    id = models.IntegerField(primary_key=True)
    intitule = models.TextField()
    type_record = models.CharField(max_length=1, choices=TYPE_RECORD_CHOICES)
    duree = models.TextField()
    notes = models.TextField(null=True, blank=True)
    resume = models.TextField(null=True, blank=True)
    time_stamp = models.DateTimeField(auto_now=True)  # on update CURRENT_TIMESTAMP
    parent = models.ForeignKey(VideoVolume)
    mime_type = models.CharField(max_length=192, null=True, blank=True)  # à calculer sur l'action save
    # supprime = models.IntegerField(default=0)  # mettre à 1 pour action delete
    technicien = models.ForeignKey(User)
    confidentialite_record = models.CharField(max_length=1, choices=CONFIDENTIALITE_RECORD_CHOICES)
    video = models.FileField(upload_to="videos", null=True, blank=True)
    video_ext = models.FileField(upload_to="videos/ext", null=True, blank=True)
    video_int = models.FileField(upload_to="videos/int", null=True, blank=True)

    # unused fields
    #temp_file_name = models.CharField(max_length=384, null=True, blank=True)  # doublon avec champ video
    #archived_file_name = models.CharField(max_length=192, null=True, blank=True)  # doublon avec champ video
    #type = models.IntegerField(null=True, blank=True)  # ??? visiblement inutilisé, toujours = 0 **N EST PAS** TYPE_EVENEMENT
    #archived = models.IntegerField(null=True, blank=True)  # bientot plus utilisé
    #online = models.IntegerField(null=True, blank=True)  # bientot plus utilisé
    #old_x = models.IntegerField(null=True, blank=True)  # bientot plus utilisé
    #old_y = models.IntegerField(null=True, blank=True)  # bientot plus utilisé
    #new_x = models.IntegerField(null=True, blank=True)  # bientot plus utilisé
    #new_y = models.IntegerField(null=True, blank=True)  # bientot plus utilisé

    def __unicode__(self):
        return self.intitule

    class Meta:
        db_table = u'video_record'


class VideoRecordCollectivite(models.Model):
    '''
    VideoRecordCollectivite model

    * datamodel review by sam
    * 0 inconsistant/unused fields
    * MD : OK
    '''
    id = models.IntegerField(primary_key=True)
    video_record = models.ForeignKey(VideoRecord)  # supprimer les lignes liées à video_record = 0
    collectivite = models.ForeignKey(Collectivite)

    class Meta:
        db_table = u'video_record_collectivite'


class VideoRecordPersonneRole(models.Model):
    '''
    VideoRecordPersonneRole model

    * datamodel review by sam
    * 0 inconsistant/unused fields
    * MD ACTION DONE : supprimer les lignes liées à video_record = 0
    '''
    id = models.IntegerField(primary_key=True)
    video_record = models.ForeignKey(VideoRecord)  # supprimer les lignes liées à video_record = 0
    personne = models.ForeignKey(Personne)
    role = models.ForeignKey(Role)

    class Meta:
        db_table = u'video_record_personne_role'


class VideoSet(models.Model):
    '''
    VideoSet model

    * datamodel review by sam
    * 0 inconsistant/unused fields
    * MD ACTION DONE : sous titres/notes/resume (vide--> NULL)
    * MD ACTION DONE : parent (0 --> NULL)
    '''
    id = models.IntegerField(primary_key=True)
    # supprime = models.IntegerField(default=0)  # mettre à 1 pour action delete
    intitule = models.CharField(max_length=255)
    sous_titre = models.CharField(max_length=384, null=True, blank=True)  # possiblement inutilisé mais utilisable, on garde pour le moment
    parent = models.ForeignKey('self', null=True, blank=True)  # lorsque c 0 passer à NULL pour consistance des données
    time_stamp = models.DateTimeField(auto_now=True)
    date_debut = models.DateField(null=True, blank=True)
    date_fin = models.DateField(null=True, blank=True)
    notes = models.TextField(null=True, blank=True)
    resume = models.TextField(null=True, blank=True)

    def __unicode__(self):
        return self.intitule

    class Meta:
        db_table = u'video_set'


# VOLUME


class Volume(models.Model):
    """
    Volume class

    Used to describe a collection of audio, named 'Partie' (!)
    * datamodel review by sam
    * REVOIR UNUSED FIELDS
    * MD CHECK DONE : 9 unused fields
    * MD ACTION DONE : parent_id/technicien_id (0 --> NULL)
    * MD ACTION DONE : notes/resume/note2prog_id/old_id (vide --> NULL)
    * MD ACTION DONE : date (0000-00-00 --> NULL)
    """
    VOLTYPE_CHOICES = (
        ('1', '1 pour champs voltype ! a quoi cela sert'),
    )
    PRE_CHOICES = (
        ('0', '0'),#0 pour champs pret ! a quoi cela sert'
        ('1', '1'),#1 pour champs pret ! a quoi cela sert
    )
    ETAT_COLLECTION_CHOICES = (
        ('0', '0'),#0 pour champs etat collection ! a quoi cela sert
        ('1', '1'),#1 pour champs etat collection ! a quoi cela sert
    )
    ETAT_ARCHIVE_CHOICES = (
        ('1', '1'),#1 pour champs etat archive ! a quoi cela sert
    )
    CONFIDENTIALITE_VOLUME_CHOICES = (
        ('0', '0'),#0 pour champs etat confidentialite volume ! a quoi cela sert
    )
    PENDING_CHOICES = (
        ('0', '0'),#0 pour champs pending ! a quoi cela sert
        ('1', '1'),#1 pour champs pending ! a quoi cela sert
        ('2', '2'),#2 pour champs pending ! a quoi cela sert
    )
    id = models.CharField(max_length=36, primary_key=True)
    old_id = models.CharField(max_length=384, null=True, blank=True)
    voltype = models.CharField(max_length=1, choices=VOLTYPE_CHOICES)
    date = models.DateField(null=True, blank=True)
    notes = models.TextField(null=True, blank=True)  # mix de NULL et ''vide a uniformiser
    resume = models.TextField(null=True, blank=True)
    note2prog_id = models.CharField(max_length=30, null=True, blank=True)
    # fk ? Cf Sandra
    # réponse : lien vers notice FLORA (a l'époque LORIS) : Sandra rempli id dans Flora puis dans Archiprod
    time_stamp = models.DateTimeField(auto_now=True)
    parent = models.ForeignKey(Evenement, null=True, blank=True)  # ceux qui valent 0 ! ?
    date_transfert = models.DateField(null=True, blank=True)
    pret = models.CharField(max_length=1, choices=PRE_CHOICES)
    # supprime = models.IntegerField(default=0)
    technicien = models.ForeignKey(User, null=True, blank=True)
    lieu = models.ForeignKey(Lieu, null=True, blank=True)
    horaire = models.CharField(max_length=15)
    etat_collection = models.CharField(max_length=1, choices=ETAT_COLLECTION_CHOICES)
    etat_archive = models.CharField(max_length=1, choices=ETAT_ARCHIVE_CHOICES)
    confidentialite_volume = models.CharField(max_length=1, choices=CONFIDENTIALITE_VOLUME_CHOICES)
    pending = models.CharField(max_length=1, choices=PENDING_CHOICES)

    # unused fields
    #auteur = models.TextField(null=True, blank=True)
    #intitule = models.TextField(null=True, blank=True)  # tjrs vide actuellement (passer à null ?)
    #label = models.TextField(null=True, blank=True)  # deja NULL
    #annee = models.TextField(null=True, blank=True)  # deja NULL
    #url = models.TextField(null=True, blank=True)  # tjrs NULL
    #doris_key = models.IntegerField(default=0)  # tjrs 0
    #cddb = models.CharField(max_length=24, db_column='CDDB', null=True, blank=True)  # tjrs a 0 !

    #for new archiprod
    sous_titre = models.CharField(max_length=384, null=True, blank=True)
    tag_evenements = models.ManyToManyField(TagEvenement, null=True, blank=True)
    type_evenement = models.ForeignKey(TypeEvenement, null=True, blank=True)
    saison = models.ForeignKey(Saison, null=True, blank=True)

    # for new schema
    evenement2 = models.ForeignKey(Evenement2, null=True, blank=True)
    intitule = models.TextField(null=True, blank=True)

    def __unicode__(self):
        return self.intitule

    class Meta:
        db_table = u'volume'


class VolumeCollectivite(models.Model):
    '''
    VolumeCollectivite model

    * datamodel review by sam
    * 0 inconsistant/unused fields
    * MD : OK
    '''
    id = models.IntegerField(primary_key=True)
    volume = models.ForeignKey(Volume)
    collectivite = models.ForeignKey(Collectivite)

    class Meta:
        db_table = u'volume_collectivite'


class VolumePersonneRole(models.Model):
    '''
    VolumePersonneRole model

    * datamodel review by sam
    * 0 inconsistant/unused fields
    * MD : OK
    '''
    id = models.IntegerField(primary_key=True)
    volume = models.ForeignKey(Volume)
    personne = models.ForeignKey(Personne)
    role = models.ForeignKey(Role)

    class Meta:
        db_table = u'volume_personne_role'


# PARTIE


class Partie(models.Model):
    '''
    Partie model

    * datamodel review by sam
    * 9 inconsistant/unused fields
    * MD ACTION DONE : titre/resume (vide --> NULL)
    * MD ACTION DONE : oeuvre_id/editeur_partition_id (0 --> NULL)
    * MD ACTION DONE : duree faire le nettoyage entre 00:00:00 et vide --> NULL
    '''
    PARTYPE_CHOICES = (
        ('0', '1 pour champs partype ! a quoi cela sert'),
    )
    CONFIDENTIALITE_PARTIE_CHOICES = (
        ('0', '0 pour champs etat confidentialite partie ! a quoi cela sert'),
        ('1', '1 pour champs etat confidentialite partie ! a quoi cela sert'),
    )
    id = models.CharField(max_length=36, primary_key=True)
    seq = models.IntegerField()
    volume = models.ForeignKey(Volume, null=True, blank=True)
    titre = models.TextField(null=True, blank=True)
    duree = models.TextField(null=True, blank=True)  # faire le nettoyage entre 00:00:00 et vide
    notes = models.CharField(max_length=765, null=True, blank=True)
    time_stamp = models.DateTimeField(auto_now=True)
    oeuvre = models.ForeignKey(Oeuvre, null=True, blank=True)
    editeur_partition = models.ForeignKey(Collectivite, null=True, blank=True)
    confidentialite_partie = models.CharField(max_length=1, choices=CONFIDENTIALITE_PARTIE_CHOICES)
    # supprime = models.IntegerField(default=0)
    audio = models.FileField(upload_to="audios", null=True, blank=True)
    audio_ext = models.FileField(upload_to="audios/ext", null=True, blank=True)
    audio_int = models.FileField(upload_to="audios/int", null=True, blank=True)

    # unused fields
    #doris_key = models.IntegerField(default=0)  # y a t'il une utilité a cette clef qui vaut tjrs 0
    #partype = models.CharField(max_length=1, choices=PARTYPE_CHOICES)
    #auteur1 = models.IntegerField(null=True, blank=True)
    #auteur2 = models.IntegerField(null=True, blank=True)
    #auteur3 = models.IntegerField(null=True, blank=True)
    #auteur4 = models.IntegerField(null=True, blank=True)
    #brahms_key = models.CharField(max_length=27, null=True, blank=True)
    #resume = models.TextField(null=True, blank=True)

    def __unicode__(self):
        return self.id

    class Meta:
        db_table = u'partie'
        ordering = ['seq', ]


class PartieCollectivite(models.Model):
    '''
    PartieCollectivite model

    * datamodel review by sam
    * 0 inconsistant/unused fields
    * MD : OK
    '''
    id = models.IntegerField(primary_key=True)
    partie = models.ForeignKey(Partie)
    collectivite = models.ForeignKey(Collectivite)

    class Meta:
        db_table = u'partie_collectivite'


class PartiePersonneRole(models.Model):
    '''
    PartiePersonneRole model

    * datamodel review by sam
    * 0 inconsistant/unused fields
    * MD : OK
    '''
    id = models.IntegerField(primary_key=True)
    partie = models.ForeignKey(Partie)
    personne = models.ForeignKey(Personne)
    role = models.ForeignKey(Role)

    class Meta:
        db_table = u'partie_personne_role'
