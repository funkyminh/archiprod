# -*- coding: utf-8 -*-
import os
import string
import factory
import datetime
from factory import fuzzy

from django.contrib.auth.models import User
from django.contrib.auth.hashers import make_password


# Factories, only used for testing purposes
# especially generate data for tests.


class UserFactory(factory.django.DjangoModelFactory):
    FACTORY_FOR = User

    username = factory.Sequence(lambda n: "user %s" % n)
    email = factory.LazyAttribute(lambda o: '%s@example.org' % o.username)

    @classmethod
    def _prepare(cls, create, password=None, **kwargs):
        return super(UserFactory, cls)._prepare(
            create,
            password=make_password(password),
            **kwargs
        )


class MediaFactory(factory.django.DjangoModelFactory):
    FACTORY_FOR = 'archives.Media'
    file = factory.django.FileField(from_path=os.path.join(os.path.dirname(__file__),
                                                           'tests/data/video.mov'))
    title = fuzzy.FuzzyText(chars=string.printable)
    summary = fuzzy.FuzzyText(length=500, chars=string.printable)

class ArchiveFactory(factory.django.DjangoModelFactory):
    FACTORY_FOR = 'archives.Archive'

    title = fuzzy.FuzzyText(chars=string.printable)
    date = fuzzy.FuzzyDate(datetime.date(1978, 1, 1))


class SetFactory(factory.django.DjangoModelFactory):
    FACTORY_FOR = 'archives.Set'

    label = fuzzy.FuzzyText(chars=string.printable)


class EventFactory(factory.django.DjangoModelFactory):
    FACTORY_FOR = 'events.Event'
