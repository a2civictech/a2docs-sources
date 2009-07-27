from django.shortcuts import render_to_response

from django.template import Context
from django.template.defaultfilters import slugify
from django.template.loader import get_template
from django.http import HttpResponse, Http404, HttpResponseRedirect

from django import forms
from django.forms import ModelForm
from django.forms.models import modelformset_factory

from foialist.models import *
from foialist.helpers import *
from foialist.secret import *

from scribd import *
import scribd
import zipfile
import os


class FileForm(ModelForm):
    class Meta:
        model = File
        exclude = ('belongs_to', 'size')
    
        
class EntryForm(ModelForm):
    
    entity = forms.CharField()
    
    class Meta:
        model = Entry
        exclude = ('slug', 'poster_slug', 'show', 'date_posted')
        
        
def f(request):
    FileFormSet = modelformset_factory(
        File, 
        form=FileForm, 
        exclude = ('belongs_to', 'size', 'name', 'scribd_link', 'scribd_id', 'scribd_ak'), 
        extra=0
    )
    
    if request.method == "POST":
        
        '''
        entry used for debug
        archname derived from entry
        
        in real use, would get this from the original article create form.
        '''
        entry = Entry.objects.get(id=1)
        archname = str(entry.id) + ".zip"
        
        # create formset instances from the data
        file_formset  = FileFormSet(request.POST, request.FILES, prefix='files')
        
        if file_formset.is_valid():
            
            scribd.config(SCRIBD_KEY, SCRIBD_SEC)
            scribd_user = scribd.login(SCRIBD_USER, SCRIBD_PASS)
            
         #   z = zipfile.ZipFile(archname, 'a')
            
            instances = file_formset.save(commit=False)
                
            for instance in instances:
                instance.belongs_to = entry
                instance.name = ""
                instance.size = ""
                instance.scribd_link = ""
                instance.scribd_id = ""
                instance.scribd_ak = ""
                instance.save()  
                
                f = instance.theFile
                
                #upload it to scribd
                scribd_doc = scribd_user.upload(f)
                instance.scribd_id = str(scribd_doc._get_id())
                instance.scribd_link = scribd_doc.get_scribd_url()
                instance.scribd_ak = scribd_doc.access_key
                
                instance.size = convert_bytes(instance.theFile.size)
                instance.name = instance.theFile.name.split("/")[-1]
                instance.save()
                
                #add it to the zip
                 
           #     z.write(f, f.name)
                       
            return HttpResponseRedirect('/doc/' + str(entry.id)) 
                          
        else: #form submission is invalid
            return render_to_response('f.html', {
            'fileform'  : file_formset,
            } )
            
        return render_to_response('f.html', {
             'fileform'  : file_formset,
             } )
        

    # BLANK ENTRY FORM
    else: 
        file_formset  = FileFormSet(prefix='files')

        return render_to_response('f.html', {
             'fileform'  : file_formset,
             } )
    
            
        
    

    # SUBMIT A DOCUMENT
    # ======================
def add(request):

    EntryFormSet = modelformset_factory(
        Entry, 
        form=EntryForm, 
        exclude = ('slug', 'show', 'date_posted', 'poster_slug'), 
        extra=0
    )
   
    FileFormSet = modelformset_factory(
        File, 
        form=FileForm, 
        exclude = ('belongs_to', 'scribd_link', 'scribd_ak', 'size', 'scribd_id', 'name'), 
        extra=2
    )
    
    
    if request.method == "POST":
        
        # create formset instances from the data
        entry_formset = EntryFormSet(request.POST, request.FILES, prefix='entries')
        file_formset  = FileFormSet(request.POST, request.FILES, prefix='files')
        
        if (entry_formset.is_valid() & file_formset.is_valid()):
                        
            # Creates a new Entity if the string doesn't match an existing entity.  
            # (we're getting this data in as text)  
            entity_name = request.POST['entries-0-entity']
            try:
                entity = Entity.objects.get(name=entity_name)
            except Entity.DoesNotExist:
                entity = Entity(name=entity_name)
                entity.slug = slugify(entity.name)
                entity.save()
                request.POST['entries-0-entity'] = entity
                
            '''  
            Here I use some ugly trickery to go around the modelformset, because I can't 
            figure out how to access modelformset values directly before saving.
             Will be fairly prone to breakage from naming scheme changes.     
            '''
            
            # doesn't work: 
            # TypeError: 'EntryFormFormSet' object does not support item assignment
            entry_formset['entries-0-entity'] = entity
            entry = entry_formset.save( commit=False)
            
            
            entry.date_posted = datetime.datetime.now() 
            # not caring about unqiue slugs yet:
            entry.slug = slugify(entry_formset.title)
            entry.poster_slug = slugify(entry_formset.poster)
            
            # show will be used for moderation (to hide questionable documents)
            entry.show = True
            
            entry.save()
            
                
            # for file_form in file_formset:
                # run some code to save the file
                # upload the docs to scribd
            
            return HttpResponseRedirect('/doc/' + str(entry.id)) 

        else: #form submission is invalid
           
            entitylist = entities()
        
            return render_to_response('add.html', {
                'entryform' : entry_formset, 
                'fileform'  : file_formset,
                'entities'  : entitylist,
                } )
                
   
   # BLANK ENTRY FORM
    else: 
        entry_formset = EntryFormSet(prefix='entries')
        file_formset  = FileFormSet(prefix='files')
        entitylist = entities()
        print entry_formset
        return render_to_response('add.html', {
            'entryform' : entry_formset, 
            'fileform'  : file_formset,
            
            'entities'  : entitylist,
            } )
