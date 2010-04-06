import os.path
from django.conf import settings
from django.contrib.syndication.feeds import Feed
from django.core.urlresolvers import reverse
from framefeed.models import default_model
from framefeed.utils import root_url


class PhotoPostsFeed(Feed):
    title = getattr(settings, "FRAMEFEED_TITLE", "Framefeed")
    feed_copyright = getattr(settings, "FRAMEFEED_COPYRIGHT", "All rights reserved")
    
    def link(self):
        return root_url() + reverse("framefeed_index")
    
    def items(self):
        return default_model.objects.published()

    def item_title(self, item):
        return item.get_feed_title()

    def item_description(self, item):
        return item.get_feed_text()

    def item_link(self, item):
        return root_url() + reverse("framefeed_post", args=[item.slug, item.id])

    def item_enclosure_url(self, item):
        return root_url() + item.medium_img.url

    def item_enclosure_length(self, item):
        return item.medium_img.file.size

    def item_enclosure_mime_type(self, item):
        file_ext = os.path.basename(item.medium_img.file.name).split('.')[-1].lower()
        if 'jpg' == file_ext:
            return 'image/jpeg'
        else:
            return 'unknown'

    def item_pubdate(self, item):
        return item.publish_at

    def item_categories(self, item):
        return item.get_tags_list()
