# -*- coding: utf-8 -*-
import datetime
from south.db import db
from south.v2 import DataMigration
from django.db import models
from django.db import connection, transaction


class Migration(DataMigration):

    def forwards(self, orm):
        "Write your forwards methods here."
        cursor1 = connection.cursor()
        cursor1.execute("insert into `utils_collectivity` (id, `name`) select t2.`id`, t2.`nom` from `collectivite` as t2")

        cursor2 = connection.cursor()
        cursor2.execute("insert into `utils_work` (id, title, subtitle, year) select t2.`id`, t2.`titre`, t2.`sous_titre`, t2.`annee` from `oeuvre` as t2")

        cursor3 = connection.cursor()
        cursor3.execute("insert into `utils_role` (id, label) select t2.`id`, t2.`intitule` from `role` as t2")

        cursor4 = connection.cursor()
        cursor4.execute("insert into `utils_person` (id, first_name, last_name) select t2.`id`, t2.`prenom`, t2.`nom` from `personne` as t2")

        cursor5 = connection.cursor()
        cursor5.execute("insert into `utils_place` (id, name, hall, country, city) select t2.`id`, t2.`nom`, t2.`salle`, t2.`pays`, t2.`ville` from `lieu` as t2;")

        cursor6 = connection.cursor()
        cursor6.execute("insert into `utils_composer` (id, `person_id`,`role_id`, `work_id`) select t2.`id`, t2.`personne_id`, t2.`role_id`, t2.`oeuvre_id` from `oeuvre_personne_role` as t2")

        transaction.commit_unless_managed()

    def backwards(self, orm):
        pass

    models = {
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

    complete_apps = ['utils']
    symmetrical = True
