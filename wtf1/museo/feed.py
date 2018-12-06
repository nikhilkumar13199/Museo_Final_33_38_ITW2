from django.contrib.syndication.views import Feed
from django.urls import reverse
from .models import latest_posts


class LatestEntriesFeed(Feed):
    title = "Latest Posts"
    link = "/museo/feed"
    description = "New articles on museo!"

    def items(self):
        return latest_posts.objects.all().order_by('-pid')[:5]
        #this return first five row from bottom ordered by pid in descending order
        #this is stored in items

    def item_title(self, item):
        return item.pid

    def item_description(self, item):
        return item.content

    def item_link(self, item):
        return reverse('museo:feed')