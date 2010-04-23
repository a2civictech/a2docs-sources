from django.conf import settings
from django.conf.urls.defaults import *
from django.contrib import admin

from foialist.views import * 

from foialist.feeds import *

feeds = {
    'recent': RecentEntries,
}


admin.autodiscover()

urlpatterns = patterns('',
    ('^$', home),
    # for pagination of collections of documents:
    (r'^page/(?P<page_number>\d+)/$', page), 
    
    # upload a document
    ('^add/$', add),
    
    # browse collections of documents
    (r'^doc/(\d+)/$', page_by_id),
    # and individual documents in a collection (uses scribd API)
    (r'^doc/(?P<eid>\d+)/view/(?P<did>\d+)/$', scribd_view),
        
    # list originating organizations
    (r'^origin/$', origins),
    # browse by originitating organiztion (ex. City of Ann Arbor)
    (r'^origin/(?P<slug>[-\w]+)/$', by_origin),
    
    # list all people who have submitted collections:
    (r'^submitter/$', posters),
    # view collections from a specific person:
    (r'^submitter/(?P<slug>[-\w]+)/$', by_poster),
    
    ('^search/$', search),    
    (r'^feeds/(?P<url>.*)/$', 
        'django.contrib.syndication.views.feed', 
        {'feed_dict': feeds}),
    
    (r'^admin/(.*)', admin.site.root),
    # add urls for /year/month
)

if settings.LOCAL_DEVELOPMENT:
    urlpatterns += patterns("django.views",
        url(r"^assets/(?P<path>.*)$", 'static.serve', {
            "document_root": settings.MEDIA_ROOT,})
    )
