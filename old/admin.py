# -*- coding: utf-8 -*-
from django.contrib import admin
from old.models import *


class VolumePersonneRoleInline(admin.TabularInline):
    model = VolumePersonneRole
    #raw_id_fields = ("personne",)
    #readonly_fields = ('personne',)
    #max_num=4
    extra=0


class VolumeCollectiviteInline(admin.TabularInline):
    model = VolumeCollectivite
    extra = 0


class PartieInline(admin.TabularInline):
    model = Partie
    extra = 0


class VideoRecordInline(admin.TabularInline):
    model = VideoRecord
    extra = 0
    exclude = ('id', 'supprime', 'confidentialite_record', 'type_record', 'archived_file_name', 'temp_file_name', 'mime_type', 'old_x', 'old_y', 'new_x', 'new_y')


class ContratAdmin(admin.ModelAdmin):
    list_display = ('id', 'intitule')


class EvenementAdmin(admin.ModelAdmin):
    list_display = ('id', 'intitule', 'sous_titre', 'parent', 'type', 'date_debut', 'date_fin')


def intitule(obj):
    return "%s" % (obj.parent.intitule,)
    intitule.short_description = 'Intitule'


class VolumeAdmin(admin.ModelAdmin):
    list_display = ('id', intitule, 'date', 'date_transfert',
        'pret', 'etat_collection')
    list_filter = ('technicien__nom',)
    date_hierarchy = 'date'
    search_fields = ['id', 'parent__intitule']
    #list_select_related = True

    inlines = [
        VolumeCollectiviteInline,
        VolumePersonneRoleInline,
        PartieInline,
    ]

    def queryset(self, request):
        qs = super(VolumeAdmin, self).queryset(request)
        return qs.exclude(supprime=1).exclude(parent__supprime=1)


class VideoAdmin(admin.ModelAdmin):
    list_display = ('id', intitule, 'date')
    list_filter = ('technicien__nom',)
    date_hierarchy = 'date'
    search_fields = ['id', 'parent__intitule']
    #list_select_related = True
    readonly_fields = ('id',)
    exclude = ('supprime', 'sort', 'type')

    inlines = [
        VideoRecordInline,
    ]

    def queryset(self, request):
        qs = super(VideoAdmin, self).queryset(request)
        return qs.exclude(supprime=1).exclude(parent__supprime=1).filter(type=1)


'''
admin.site.register(Volume, VolumeAdmin)
admin.site.register(Evenement, EvenementAdmin)
admin.site.register(Partie)
admin.site.register(Lieu)
admin.site.register(Personne)
admin.site.register(Role)
admin.site.register(Collectivite)
admin.site.register(Utilisateur)
admin.site.register(Contrat, ContratAdmin)
admin.site.register(NoteProgramme)
admin.site.register(VideoVolume, VideoAdmin)
'''
