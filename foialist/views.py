from django.conf import settings
from django.forms.models import modelformset_factory
from django.http import HttpResponse, Http404, HttpResponseRedirect
from django.shortcuts import render_to_response
from django.template import Context
from django.template.loader import get_template

from foialist.forms import * 
from foialist.helpers import *
from foialist.models import * 

import datetime
from scribd import *
import scribd

'''
TODO

- Implement actual uploading
- Write about text
- Replace owl

'''

def add(request):
    context = {}
    entry_form = EntryForm(prefix='entries')
    file_forms_excludes = ('belongs_to', 'scribd_link', 'scribd_ak', 'size', 
                           'scribd_id', 'name')
    FileFormSetFactory = modelformset_factory(File, form=FileForm, extra=2,
                                        exclude=file_forms_excludes,)
    file_formset = FileFormSetFactory(prefix='files')
    
    if request.method == 'POST':
        entry_form = EntryForm(request.POST, request.FILES, prefix='entries')
        file_formset = FileFormSetFactory(request.POST, request.FILES, 
                                          prefix='files')
    
        if entry_form.is_valid() and file_formset.is_valid():
            # saving the entry form is easy
            entry = entry_form.save()
            
            # saving the files - more involved
            scribd.config(settings.SCRIBD_KEY, settings.SCRIBD_SEC)
            scribd_user = scribd.login(settings.SCRIBD_USER, 
                                       settings.SCRIBD_PASS)
            
            for f in file_formset.save(commit=False):
                f.belongs_to = entry
                f.name = ""
                f.size = ""
                f.scribd_link = ""
                f.scribd_id = ""
                f.scribd_ak = ""
                f.save()  
                
                # attempt to upload it to scribd
                try:
                    scribd_doc = scribd_user.upload(f.theFile)
                    f.scribd_id = str(scribd_doc._get_id())
                    f.scribd_link = scribd_doc.get_scribd_url()
                    f.scribd_ak = scribd_doc.access_key
                except scribd.ResponseError:
                    pass
                
                f.size = convert_bytes(f.theFile.size)
                f.name = f.theFile.name.split("/")[-1]
                f.save()
    
    context['fileform'] = file_formset
    context['entryform'] = entry_form
    context['entities'] = entities()
    return render_to_response('add.html', context)

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