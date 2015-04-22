# -*- coding: utf-8 -*-
import base64
import requests
import datetime

from django.http import HttpResponse, StreamingHttpResponse, Http404
from django.contrib.sites.models import Site
from django.contrib.auth.decorators import login_required
from django.core.mail import send_mail, EmailMessage
from django.db.models import Q
from django.shortcuts import render_to_response, get_object_or_404, get_list_or_404
from django.template import RequestContext
from django.utils.translation import ugettext as _

import haystack.views

from archives.forms import CustomSearchForm, UploadForm
from archives.models import Media
from events.models import EventType


def detail(request, slug):
    """
    Display one media
    """
    form = CustomSearchForm()
    media = get_object_or_404(Media, slug=slug)
    if media.archive is None:
        other_archive_medias = None
    else:
        other_archive_medias = Media.objects.filter(archive=media.archive).order_by('order')
        # Test if current media is the only media in the archive
        # so we don't need to have the related archive medias
        if other_archive_medias.count() == 1:
            other_archive_medias = None
    return render_to_response('archives/detail.html',
                              {'form': form, 'media': media, 'slug': slug,
                               'other_archive_medias': other_archive_medias},
                              context_instance=RequestContext(request))


def home(request):
    """
    Home view
    """
    form = CustomSearchForm()
    medias = []
    # Latest workshop
    # get childs of event type id 32
    descendant_ids = EventType.objects.get(id=32).get_descendants(include_self=True).values_list('id', flat=True)
    w_medias = get_list_or_404(Media.objects.order_by('-archive__date'), archive__event__event_type__id__in=descendant_ids)[0]
    w_medias.bloc_title = u"Workshops"
    w_medias.see_others = u'selected_facets=event_type_exact:Séminaire / Conférence'
    medias.append(w_medias)
    # Latest concert
    c_medias = get_list_or_404(Media.objects.order_by('-time_stamp'), work__isnull=False)[0]
    c_medias.bloc_title = u"Concerts"
    c_medias.see_others = 'selected_facets=is_sound_exact:true'
    medias.append(c_medias)
    # "Images d'une œuvre"
    i_medias = get_list_or_404(Media.objects.order_by('-archive__date'), archive__set__id__in=[3220])[0]
    i_medias.bloc_title = u"Images d'une œuvre"
    i_medias.see_others = 'selected_facets=set_exact:Images d\'une œuvre (série documentaire)'
    medias.append(i_medias)
    # Other
    o_medias = Media.objects.order_by('-archive__date').exclude(archive__event__event_type__id__in=descendant_ids).exclude(work__isnull=False).exclude(archive__set__id__in=[3220])[0]
    o_medias.bloc_title = u"Others"
    o_medias.see_others = False
    medias.append(o_medias)
    return render_to_response('archives/home.html',
                              {'form': form, 'medias': medias, 'home':True},
                              context_instance=RequestContext(request))


class CustomSearchView(haystack.views.FacetedSearchView):
    """
    CustomSearchView subclass Haystack FacetedSearchView in order
    to add query string filter in the context
    to keep it between next and prev pages
    """

    def build_page(self):
        paginator, page = super(CustomSearchView, self).build_page()
        page.page_num = int(self.request.GET.get('page', 1))
        page.query = self.request.GET.get('q', '')
        page.show_all = False
        page.multi_page = True
        page.can_show_all = False
        data =  self.request.GET.copy()
        if 'q' in data: del data['q']
        if 'page' in data: del data['page']
        page.filters_query_string = data.urlencode()
        return (paginator, page)

    def clean_filters(self):
        """Returns a list of tuples (filter, value) of applied facets"""
        filters = []
        # get distinct facets
        facets = list(set(self.form.selected_facets))
        for facet in facets:
            if ":" not in facet:
                continue
            field, value = facet.split(":", 1)
            field = _(field.replace('_', ' ').replace('exact', '')).title()
            print field
            filters.append((field, value))
        return filters

    def extra_context(self):
        extra = super(CustomSearchView, self).extra_context()
        extra['filters'] = self.clean_filters()
        # This "clean" the extra['facets']['fields'] dict
        # to remove haystack faceting results which has 0 results
        for key, val in extra['facets']['fields'].items():
            extra['facets']['fields'][key] = [item for item in val if item[1] > 0]
        data =  self.request.GET.copy()
        extra['facets']['fields']['year'] = sorted(extra['facets']['fields']['year'], key=lambda tup: tup[0], reverse=True)
        if 'q' in data: del data['q']
        if 'page' in data: del data['page']
        extra['filters_query_string'] = data.urlencode()
        print '>>>>', extra['filters_query_string']
        return extra


def embed_media(request, slug):
    # Here, we use the admin_objects manager for embed
    # This allow us to get all objects, including the ones we can't broadcast
    # but we want to be able to include inside other website (like Repertoire/Analyse.
    media = get_object_or_404(Media.admin_objects, slug__istartswith=slug)
    return render_to_response('archives/embed.html',
                              {'media': media},
                              context_instance=RequestContext(request))

def playlist(request):
    if request.GET:
        q_object = Q()
        for slug in request.GET.getlist('slug'):
            q_object.add(Q(slug__istartswith=slug), Q.OR)
        medias = Media.objects.filter(q_object)
        print medias
        format = request.GET.get('format', None)
        if format == 'jwplayer':
            return render_to_response('archives/playlist-jwplayer.html',
                                      {'medias': medias},
                                      context_instance=RequestContext(request))


def download(request, text):
    data = base64.b64decode(text).split('||')
    url = 'http://%s%s' % (Site.objects.get_current().domain, data[0])
    limit_date = datetime.datetime.strptime(data[1], '%Y-%m-%d %H:%M:%S.%f')+datetime.timedelta(days=30)
    if limit_date < datetime.datetime.now():
        raise Http404

    filename = url.split('/')[-1]
    my_data = requests.get(url, stream=True)

    response = StreamingHttpResponse(my_data.iter_content(), mimetype='application/octet-stream')
    response['Content-Disposition'] = 'attachment; filename="%s"' % filename
    return response

@login_required
def upload(request):
    upload_form = UploadForm()
    if request.method == 'POST':
        upload_form = UploadForm(request.POST, request.FILES)
        if upload_form.is_valid():
            description = upload_form.cleaned_data['description']
            broadcastable = upload_form.cleaned_data['broadcastable']
            file = upload_form.cleaned_data['file']
            authorization = upload_form.cleaned_data['authorization']
            # TODO: should use Media.CONFIDENTIALITE_PARTIE_CHOICES
            user = request.user
            media = Media(comments=description, user=user, file=file, confidentiality="2")
            media.save()
            mail = EmailMessage('[medias.ircam.fr] New media upload', 'New media, id: %s - broadcastable: %s' % (media.id, broadcastable), "medias@ircam.fr", ["Sandra.El-Fakhouri@ircam.fr", "Eric.de.Gelis@ircam.fr"])
            if authorization:
                mail.attach(authorization.name, authorization.read(), authorization.content_type)
            mail.send()
            return render_to_response('archives/upload-end.html', {'media': media}, context_instance = RequestContext(request))
    return render_to_response('archives/upload.html', {'upload_form': upload_form}, context_instance = RequestContext(request))

