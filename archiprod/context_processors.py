from django.contrib.sites.models import Site

def is_archiprod(request):
    """ Context processor to set archiprod to True for the main ressource menu """
    return {'archiprod': True}

def in_situ(request):
	""" Context processor to set in_situ to True if user is in situ """
	return {'in_situ': request.in_situ}

def site(request):
    """ Context processor to get current site, (and base url)"""
    return {
        'site': Site.objects.get_current()
    }
