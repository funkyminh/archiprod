class VideoVolume(models.Model):
    """
    VideoVolume model

    * datamodel review by sam
    * 0 inconsistant/unused fields
    * MD ACTION DONE : intitulé/notes/resume (vide--> NULL)
    * MS ACTION DONE : parent (0 --> NULL)
    * MD ACTION DONE : date passer 0000-00-00 à NULL
    """
    id = models.CharField(max_length=12, primary_key=True)
    title = models.TextField(null=True, blank=True)   # intitule
    #rempli lorsque type=2
    #sinon vide lorsque type=1 et intitule video_volume provient de intitule évènement
    date = models.DateField(null=True, blank=True)   # date
    comments = models.TextField(blank=True)   # notes
    summary = models.TextField(null=True, blank=True)   # resume
    time_stamp = models.DateTimeField(auto_now=True)  # on update CURRENT_TIMESTAMP
    set = models.ForeignKey(Set, null=True, blank=True)  # passer parent=0 à parent=NULL
    order = models.CharField(max_length=12, default=None, null=True, blank=True)   # sort
    #type = models.CharField(max_length=1, choices=TYPE_CHOICES, null=True, blank=True)
    #type=NULL videos supprimées, doublon avec champ supprime=1
    #supprime = models.IntegerField(default=0)  # mettre à 1 pour action delete
    #à masquer du formulaire d'admin
    #mettre à 0 lorsqu'on sauve
    #mettre à 1 lorsque'on supprime
    user = models.ForeignKey(User, null=True, blank=True)   # technicien
    place = models.ForeignKey(Place, null=True, blank=True)   # lieu
    time = models.CharField(max_length=5,  default=None, null=True, blank=True)  # horaire de l'évènement vidéo   # horaire

    #for new archiprod
    subtitle = models.CharField(max_length=384, null=True, blank=True)   # sous_titre
    #tag_evenement = models.ForeignKey(TagEvenement, null=True, blank=True)
    tags = models.ManyToManyField(Tag, null=True, blank=True)   # tag_evenements
    #type_evenement = models.ForeignKey(TypeEvenement, null=True, blank=True)
    #saison = models.ForeignKey(Saison, null=True, blank=True)

    # for new schema
    event = models.ForeignKey(Event, null=True, blank=True)   # evenement2
    collectivities = models.ManyToManyField(Collectivity, null=True, blank=True)   # collectivites
    participants = models.ManyToManyField(Person, null=True, blank=True, through='ArchiveParticipant')   # participants

    def __unicode__(self):
        return self.id


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
    PENDING_CHOICES = (
        ('0', '0'),#0 pour champs pending ! a quoi cela sert
        ('1', '1'),#1 pour champs pending ! a quoi cela sert
        ('2', '2'),#2 pour champs pending ! a quoi cela sert
    )
    id = models.CharField(max_length=36, primary_key=True)
    old_id = models.CharField(max_length=384, null=True, blank=True)
    #voltype = models.CharField(max_length=1, choices=VOLTYPE_CHOICES)
    date = models.DateField(null=True, blank=True)
    comments = models.TextField(null=True, blank=True)  # mix de NULL et ''vide a uniformiser   # notes
    summary = models.TextField(null=True, blank=True)   # resume
    note2prog_id = models.CharField(max_length=30, null=True, blank=True)
    # fk ? Cf Sandra
    # réponse : lien vers notice FLORA (a l'époque LORIS) : Sandra rempli id dans Flora puis dans Archiprod
    time_stamp = models.DateTimeField(auto_now=True)
    set = models.ForeignKey(Set, null=True, blank=True)  # ceux qui valent 0 ! ?
    date_transfert = models.DateField(null=True, blank=True)   # date_transfert
    available = models.CharField(max_length=1, choices=PRE_CHOICES)   # pret
    #supprime = models.IntegerField(default=0)
    user = models.ForeignKey(User, null=True, blank=True)   # technicien
    place = models.ForeignKey(Place, null=True, blank=True)   # lieu
    time = models.CharField(max_length=15)   # horaire
    state = models.CharField(max_length=1, choices=ETAT_COLLECTION_CHOICES)   # etat_collection
    #etat_archive = models.CharField(max_length=1, choices=ETAT_ARCHIVE_CHOICES)   # etat_archive
    #confidentiality = models.CharField(max_length=1, choices=CONFIDENTIALITE_VOLUME_CHOICES)   # confidentialite_volume
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
    subtitle = models.CharField(max_length=384, null=True, blank=True)   # sous_titre
    tags = models.ManyToManyField(Tag, null=True, blank=True)   # tag_evenements
    #type_evenement = models.ForeignKey(TypeEvenement, null=True, blank=True)
    #saison = models.ForeignKey(Saison, null=True, blank=True)

    # for new schema
    event = models.ForeignKey(Event, null=True, blank=True)   # evenement2
    collectivities = models.ManyToManyField(Collectivity, null=True, blank=True)   # collectivites
    participants = models.ManyToManyField(Person, null=True, blank=True, through='ArchiveParticipant')
    title = models.TextField(null=True, blank=True)   # intitule attention supprime dans OLD

    def __unicode__(self):
        return self.title


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
    title = models.TextField()   # intitule
    record_type = models.CharField(max_length=1, choices=TYPE_RECORD_CHOICES)  # type_record
    duration = models.TextField()   # duree
    comments = models.TextField(null=True, blank=True)   # notes
    summary = models.TextField(null=True, blank=True)   # resume
    time_stamp = models.DateTimeField(auto_now=True)  # on update CURRENT_TIMESTAMP
    video_volume = models.ForeignKey(Archive)
    mime_type = models.CharField(max_length=192, null=True, blank=True)  # à calculer sur l'action save
    #supprime = models.IntegerField(default=0)  # mettre à 1 pour action delete
    user = models.ForeignKey(User)   # technicien
    confidentiality = models.CharField(max_length=1, choices=CONFIDENTIALITE_RECORD_CHOICES, default="0")   # confidentialite_record
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

    collectivities = models.ManyToManyField(Collectivity, null=True, blank=True)
    participants = models.ManyToManyField(Person, null=True, blank=True, through='Participant')

    def __unicode__(self):
        return self.title
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
    order = models.IntegerField()   # seq
    volume = models.ForeignKey(Archive, null=True, blank=True)
    title = models.TextField(null=True, blank=True)   # titre
    duration = models.TextField(null=True, blank=True)  # faire le nettoyage entre 00:00:00 et vide   # duree
    comments = models.CharField(max_length=765, null=True, blank=True)   # notes
    time_stamp = models.DateTimeField(auto_now=True)
    work = models.ForeignKey(Work, null=True, blank=True)   # oeuvre
    publisher = models.ForeignKey(Collectivity, null=True, blank=True)   # editeur_partition
    confidentiality = models.CharField(max_length=1, choices=CONFIDENTIALITE_PARTIE_CHOICES)   # confidentialite_partie
    #supprime = models.IntegerField(default=0)
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
    #resume = models.TextField(null=True, blank=True)`

    collectivities = models.ManyToManyField(Collectivity, null=True, blank=True)   # collectivites
    participants = models.ManyToManyField(Person, null=True, blank=True, through='Participant')

    def __unicode__(self):
        return self.title
       