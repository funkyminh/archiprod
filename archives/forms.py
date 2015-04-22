# -*- coding: utf-8 -*-
import autocomplete_light

from django import forms
from django.db.models import Count
from django.utils.translation import ugettext_lazy as _

from haystack.forms import FacetedSearchForm

from archives.models import Set, Archive
from events.models import EventType

from .models import Media


YEARS = list(set([archive.date.year for archive in Archive.objects.order_by('date') if archive.date]))
YEARS_CHOICES = [(y, y) for y in sorted(YEARS, reverse=True)]


class CustomSearchForm(FacetedSearchForm):
    """
    Custom Search Form
    """
    # Override default q field from SearchForm for design purposes
    q = forms.CharField(required=False, label="",
                        widget=forms.TextInput(attrs={'class': 'input-xxlarge search-query',
                                                      'placeholder': _(u'Search in audio/video archives')}))

    def search(self):
        return super(CustomSearchForm, self).search().highlight()


class FilterSearchForm(CustomSearchForm):
    """
    Filter Search Form
    """
    sets = forms.ModelMultipleChoiceField(queryset=Set.objects.all(),
                                          required=False, widget=forms.MultipleHiddenInput)
    #event_types = forms.ModelMultipleChoiceField(queryset=EventType.objects.all(),
    #                                             required=False, widget=forms.CheckboxSelectMultiple)
    #years = forms.MultipleChoiceField(choices=YEARS_CHOICES, required=False)
    #media_type = forms.ChoiceField(choices=(('', '----'), ('audio', 'Audio'), ('video', 'Video')), required=False)
    #is_sound = forms.BooleanField(required=False)
    date_order = forms.ChoiceField(choices=(('', '----'), ('ASC', 'Asc'), ('DESC', 'Desc')), required=False)
    #selected_facets = forms.MultipleChoiceField(widget=forms.MultipleHiddenInput)

    def search(self):
        # First, store the SearchQuerySet received from other processing.
        sqs = super(FilterSearchForm, self).search()
        # Keep a ref of initial sqs not filtered for count feature (see below)
        initial_sqs = sqs
        if not self.is_valid():
            return self.no_query_found()

        if self.cleaned_data['sets']:
            sets = self.cleaned_data['sets'].values_list('id', flat=True)
            sqs = sqs.filter(set__in=[set.label for set in Set.objects.filter(id__in=sets)])

        #if self.cleaned_data['event_types']:
        #    event_types = self.cleaned_data['event_types'].values_list('id', flat=True)
        #    sqs = sqs.filter(event_type__in=event_types)

        '''
        if self.cleaned_data['years']:
            years = self.cleaned_data['years']
            sqs = sqs.filter(year__in=years)
        '''

        #if self.cleaned_data['media_type']:
        #    media_type = self.cleaned_data['media_type']
        #    sqs = sqs.filter(media_type=media_type)

        #if self.cleaned_data['is_sound']:
        #    sqs = sqs.filter(is_sound=True)
        if self.cleaned_data['date_order']:
            order = self.cleaned_data['date_order']
            if order == 'ASC':
                sqs = sqs.order_by('year')
            else:
                sqs = sqs.order_by('-year')
        #else:
        #    sqs = sqs.order_by('-year')
        self.query = True
        #sqs_ids = [r.pk for r in initial_sqs]

        return sqs

    def no_query_found(self):
        return self.searchqueryset.all()


autocomplete_light.autodiscover()  # to be sure registry is not empty

class UploadFileFromServer(forms.Form):
    """
    Form used for uploading media files from other server
    """
    media = forms.ModelChoiceField(required=False, queryset=Media.objects.all(), widget=autocomplete_light.ChoiceWidget('MediaAutocomplete'))
    file_path = forms.CharField(max_length=100)


class UploadForm(forms.Form):
    """
    Upload media form
    """
    description = forms.CharField(label=_('Description'), widget=forms.Textarea, help_text=_('Description of the media you want to submit'))
    broadcastable = forms.BooleanField(label=_('Broadcastable'), required=False, help_text=_('Check the box if your media can be freely broadcastable'))
    file = forms.FileField(label=_('File'), help_text=_('The media file, can be either a video or an audio file.'))
    authorization = forms.FileField(label=_('Authorization'), required=False, help_text=_('Join the authorization to broadcast the media. If not provided here, send a mail to Sandra.El-Fakhouri@ircam.fr with the authorization.'))
