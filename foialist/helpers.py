from foialist.models import *

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