from django.conf import settings
from django.conf.urls.defaults import *
from django.contrib import admin

from foialist.views import * 


admin.autodiscover()

urlpatterns = patterns('',
    ('^$', home),
    ('^add/$', add),

    # ('^file/$', f),
    
    (r'^doc/(\d+)/$', page_by_id),
    (r'^doc/(?P<eid>\d+)/view/(?P<did>\d+)/$', scribd_view),
        
 #  (r'^created/$', by_creation_date),
 #  (r'^submitted/$', by_submission_date),
        
    (r'^origin/$', origins),
    (r'^origin/(?P<slug>[-\w]+)/$', by_origin),
    
    (r'^submitter/$', posters),
    (r'^submitter/(?P<slug>[-\w]+)/$', by_poster),
    
    (r'^admin/(.*)', admin.site.root),
    # add urls for /year/month
    # can I do one for people without adding another table?
        # I think so -- just convert spaces to underscores for the URL in the view.
        # then back again for the search string 
        # underscores, in case of a hyphenated last name
        # maybe there's mechanism for this already.
)

if settings.LOCAL_DEVELOPMENT:
    urlpatterns += patterns("django.views",
        url(r"^assets/(?P<path>.*)$", 'static.serve', {
            "document_root": settings.MEDIA_ROOT,})
    )
