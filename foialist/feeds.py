from django.conf import settings
from django.contrib.syndication.feeds import Feed
from foialist.models import *

class RecentEntries(Feed):
    title = "Recent documents from the Ann Arbor Gov't. Document Repository"
    link = "/"
    description = "Documents relevant to local governance."

    def items(self):
        return Entry.objects.order_by('-date_posted')[:10]