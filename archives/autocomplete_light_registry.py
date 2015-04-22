# -*- coding: utf-8 -*-
import autocomplete_light

from .models import Set, Tag, Media


class TagAutocomplete(autocomplete_light.AutocompleteModelBase):
    search_fields = ['label',]


class SetAutocomplete(autocomplete_light.AutocompleteModelBase):
    search_fields = ['label',]


class MediaAutocomplete(autocomplete_light.AutocompleteModelBase):
    search_fields = ['title', 'archive__title', 'work__title', 'id' ]


autocomplete_light.register(Tag, TagAutocomplete)
autocomplete_light.register(Set, SetAutocomplete)
autocomplete_light.register(Media, MediaAutocomplete)
