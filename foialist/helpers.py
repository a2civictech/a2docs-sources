from foialist.models import *
from foialist.views import *
from django.conf import settings
import math

def entities():
    '''
    builds a list of existing entites
    formatted as a javascript array
    for the autocomplete on the entry form.
    '''
    
    entities = Entity.objects.all()
    entitylist = "["
    for entity in entities:
         entitylist += "\"" + entity.name + "\", "
    entitylist += "]"
    
    return entitylist
    
def convert_bytes(bytes):
    bytes = float(bytes)
    if bytes >= 1099511627776:
        terabytes = bytes / 1099511627776
        size = '%.2f TB' % terabytes
    elif bytes >= 1073741824:
        gigabytes = bytes / 1073741824
        size = '%.2f GB' % gigabytes
    elif bytes >= 1048576:
        megabytes = bytes / 1048576
        size = '%.2f MB' % megabytes
    elif bytes >= 1024:
        kilobytes = bytes / 1024
        kilobytes = round(kilobytes, 0)
        size = '%.2f KB' % kilobytes
    else:
        bytes = round(bytes, 0)
        size = '%.2f bytes' % bytes
    return size

def fake_slug(string):
    '''
    returns a fake slug for URL handling
    '''
    string = string.replace(" ", "_")
    string = string.replace("/", "-")
    return string
    
def pages():
    count = float(Entry.objects.all().count())
    real_num_pages = count / settings.ITEMS_PER_PAGE
    
    # because we cannot have a fraction of a page
    # and rounding down would loose us pages
    num_pages = int(math.ceil(real_num_pages)) 
    l = range(1, num_pages + 1)
    
    return l