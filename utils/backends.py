# -*- coding: utf-8 -*-
from imapauth.backends import IMAPBackend
from django.contrib.auth.models import User


class CustomIMAPBackend(IMAPBackend):
    def authenticate(self, username=None, password=None):
        user = super(CustomIMAPBackend, self).authenticate(username, password)
        if user is None:
            return None
        # First access to admin process:
        # We give the user a default group
        # and an access to the admin interface
        changed = False
        if len(user.groups.all()) == 0:
            user.groups = [2, ]
            changed = True
        if not user.is_staff:
            user.is_staff = True
            changed = True
        if changed:
            user.save()
        user.email = "%s@ircam.fr" % (username)
        user.save()
        # TODO: This is ugly. We should return directly user
        # But, if so, the first attempt fails, as user variable
        # is not updated with its groups and is_staff
        return User.objects.get(username=username)
