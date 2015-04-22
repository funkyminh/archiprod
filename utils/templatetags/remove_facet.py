from django.template import Library
from django.utils.http import urlencode

register = Library()

@register.simple_tag
def remove_facet(request, facet_value):
    """"Returns a string that extracts the supplied facet_value's facect from
        the current querystring
    """
    params = {}
    for param in request.GET.lists():
        # reconstruct the non-selected_facets params
        if param[0] != 'selected_facets':
            for v in param[1]:
                params[param[0]] = v
        else:
            print param[0]
            for v in param[1]:
                # exclude the selected_facet param that matches the supplied
                # facet_value
                if facet_value != v.split(':')[1]:
                    params[param[0]] = v
    qs = '?%s' % urlencode(params)
    return qs
