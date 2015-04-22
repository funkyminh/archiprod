# -*- coding: utf-8 -*-
from netaddr import *


class SetRemoteAddrFromForwardedFor(object):
    """
    Middleware that sets REMOTE_ADDR based on HTTP_X_FORWARDED_FOR, if the
    latter is set. This is useful if you're sitting behind a reverse proxy that
    causes each request's REMOTE_ADDR to be set to 127.0.0.1.

    Note that this does NOT validate HTTP_X_FORWARDED_FOR. If you're not behind
    a reverse proxy that sets HTTP_X_FORWARDED_FOR automatically, do not use
    this middleware. Anybody can spoof the value of HTTP_X_FORWARDED_FOR, and
    because this sets REMOTE_ADDR based on HTTP_X_FORWARDED_FOR, that means
    anybody can "fake" their IP address. Only use this when you can absolutely
    trust the value of HTTP_X_FORWARDED_FOR.
    """
    def process_request(self, request):
        try:
            real_ip = request.META['HTTP_X_FORWARDED_FOR']
        except KeyError:
            return None
        else:
            # HTTP_X_FORWARDED_FOR can be a comma-separated list of IPs. The
            # client's IP will be the first one.
            real_ip = real_ip.split(",")[0].strip()
            request.META['REMOTE_ADDR'] = real_ip


class SetUserLocationFromAddr(object):
    """
    Middleware that sets request.in_situ = True if
    the user is located inside Ircam, based on its IP.
    """
    def process_request(self, request):
        ip = IPAddress(request.META['REMOTE_ADDR'])
        # Ircam network IP
        ipv4_network1 = IPNetwork('129.102/17')
        ipv4_network2 = IPNetwork('129.102.192/24')
        ipv6_network3 = IPNetwork('2001:0660:3004::/49')
        if ip in ipv4_network1 or ip in ipv4_network2 or ip in ipv6_network3:
            request.in_situ = True
        else:
            request.in_situ = False
