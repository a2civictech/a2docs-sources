from django.shortcuts import render_to_response
from django.template.loader import get_template
from django.template import Context
from django.http import HttpResponse, Http404, HttpResponseRedirect
from django.conf import settings

from django import forms
from django.forms import ModelForm
from django.forms.models import modelformset_factory

from foialist.models import * 
from foialist.add import *
from foialist.helpers import *

import datetime

'''
TODO

- Implement actual uploading
- Write about text
- Replace owl

'''

class CommentForm(ModelForm):
    poster = forms.CharField()
    
    class Meta:
        model = Comment
        
def count_files(entries):
    counts = {}
    for entry in entries:
        count = File.objects.filter(belongs_to=entry).count()
        counts[entry.title] = count
    return counts
    
    
    # HOMEPAGE
    # ======================
def home(request):
    entries = Entry.objects.filter(show=True)
    counts = count_files(entries)
    return render_to_response('list.html', {'entries': entries, 'counts': counts})

    
    # DISPLAY DOCS by ORIGIN
    # ======================
def origins(request):
    # takes a source ID
    # returns all documents from that source.

    entries = Entity.objects.all()
    
    return render_to_response('entities.html', {'entries': entries, })
    
    
def by_origin(request, slug):
    # takes a source ID
    # returns all documents from that source.
    
    entity = Entity.objects.get(slug=slug)
    entries = Entry.objects.filter(show=True, entity=entity)
    origin = entity.name
    
    headline = Entity.objects.get(id=entity.id).name
    
    counts = count_files(entries)
    return render_to_response('list.html', {'entries': entries, 'counts': counts, 'origin':origin})
    
    
    
    # DISPLAY DOCS by SUBMITTER
    # ======================
    
def posters(request):
    # displays all submitters and the # of contributions.

    posters = Entry.objects.filter(show=True)
    distinct_posters = Entry.objects.values('poster', 'poster_slug').distinct()
    entries = []
    for distinct_poster in distinct_posters:
        count = Entry.objects.filter(poster = distinct_poster['poster']).count()

        entry = {'slug': distinct_poster['poster_slug'], 'name': distinct_poster['poster'], 'count': str(count)}
        entries.append(entry)
    
    return render_to_response('posters.html', {'entries': entries, })
    
    
def by_poster(request, slug):
    # takes a submitter slug
    # returns all documents from that submitter.

    entries = Entry.objects.filter(show=True, poster_slug = slug)
    origin = entries[0].poster
    
    counts = count_files(entries)
    
    return render_to_response('list.html', {'entries': entries, 'origin':origin, 'counts':counts })
    
    
    # DISPLAY A PAGE BY ID
    # ======================
def page_by_id(request, pageid):
    try:
        pageid = int(pageid)
    except ValueError:
        raise Http404
        
    try:
        entry = Entry.objects.get(id=pageid)
    except Entry.DoesNotExist:
        return render_to_response('404.html', { 'message' : 'The entry could not be found.'})
       
    files = File.objects.filter(belongs_to = entry)
    file_info = []
    for f in files:
        file_info.append(f)
                  
    return render_to_response('page_by_id.html', {'e': entry, 'files': file_info})
    
def scribd_view(request, eid, did):
    '''
    did = file ID
    eid = entry id 
    '''
    f = File.objects.get(id=did)
    
    entry = Entry.objects.get(id=eid)
    files = File.objects.filter(belongs_to = entry)
    
    return render_to_response('scribd_view.html', {
        'e': entry, 
        'f': f,
        'files': files,
        'key': settings.SCRIBD_KEY
    })
    
    