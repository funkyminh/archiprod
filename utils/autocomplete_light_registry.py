# -*- coding: utf-8 -*-
from django.contrib.auth.models import User

import autocomplete_light

from .models import Person, Role, Collectivity, Place, Work, Composer


class PersonAutocomplete(autocomplete_light.AutocompleteModelBase):
    search_fields = ['^first_name', 'last_name']


class RoleAutocomplete(autocomplete_light.AutocompleteModelBase):
    search_fields = ['label',]


class CollectivityAutocomplete(autocomplete_light.AutocompleteModelBase):
    search_fields = ['name',]


class PublisherAutocomplete(autocomplete_light.AutocompleteModelBase):
    search_fields = ['name',]


class PlaceAutocomplete(autocomplete_light.AutocompleteModelBase):
    search_fields = ['name',]


class WorkAutocomplete(autocomplete_light.AutocompleteModelBase):
    search_fields = ['title', 'composers__last_name', 'composers__first_name']
    limit_choices = 500
    def choice_label(self, choice):
        """ Add composer to default rendering to ease admin work selection """
        composers = [composer.__unicode__() for composer in choice.composers.all()]
        return '<i>%s</i>, %s' % (choice.title, ', '.join(composers))

class ComposerAutocomplete(autocomplete_light.AutocompleteModelBase):
    search_fields = ['person__first_name', 'person__last_name']


class UserAutocomplete(autocomplete_light.AutocompleteModelBase):
    search_fields = ['username']


autocomplete_light.register(Person, PersonAutocomplete)
autocomplete_light.register(Role, RoleAutocomplete)
autocomplete_light.register(Collectivity, CollectivityAutocomplete)
autocomplete_light.register(Collectivity, PublisherAutocomplete)
autocomplete_light.register(Place, PlaceAutocomplete)
autocomplete_light.register(Work, WorkAutocomplete)
autocomplete_light.register(Composer, ComposerAutocomplete)
autocomplete_light.register(User, UserAutocomplete)
