# -*- coding: utf-8 -*-
import autocomplete_light

from .models import Event, EventType


class EventAutocomplete(autocomplete_light.AutocompleteModelBase):
    search_fields = ['title']


class EventTypeAutocomplete(autocomplete_light.AutocompleteModelBase):
    search_fields = ['label',]


autocomplete_light.register(Event, EventAutocomplete)
autocomplete_light.register(EventType, EventTypeAutocomplete)
