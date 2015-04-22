# -*- coding: utf-8 -*-
from haystack import indexes
from archives.models import Media


class MediaIndex(indexes.SearchIndex, indexes.Indexable):
    text = indexes.CharField(document=True, use_template=True)
    set = indexes.CharField(model_attr='archive__set__label', null=True, faceted=True)
    event_type = indexes.CharField(model_attr='archive__event__event_type__get_root', null=True, faceted=True)
    year = indexes.IntegerField(model_attr='archive__date__year', null=True, faceted=True)
    media_type = indexes.CharField(model_attr='media_type', null=True, faceted=True)
    is_sound = indexes.BooleanField(model_attr='is_sound', faceted=True)

    # fields to boost search results
    composers = indexes.MultiValueField(null=True, boost=1.225)
    participants_media = indexes.MultiValueField(null=True, boost=1.105)
    title = indexes.CharField(null=True, boost=1.125)
    work = indexes.CharField(null=True, boost=1.225)

    def prepare_composers(self, obj):
        if not obj.work:
            return None
        return ["%s %s" % (composer.first_name, composer.last_name) for composer in obj.work.composers.all()]

    def prepare_work(self, obj):
        if not obj.work:
            return None
        return "%s %s" % (obj.work.title, obj.work.subtitle)

    def prepare_participants_media(self, obj):
        return ["%s %s" % (participant.first_name, participant.last_name) for participant in obj.participants.all()]

    def prepare_title(self, obj):
        return obj.__unicode__()

    def get_model(self):
        return Media

    def index_queryset(self, using=None):
        """Used when the entire index for model is updated."""
        return self.get_model().objects.all()
