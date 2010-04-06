from django.conf.urls.defaults import *
from framefeed import views
from framefeed.feeds import PhotoPostsFeed

feeds = {'rss': PhotoPostsFeed}

urlpatterns = patterns('',
    url(r'^$', views.index, name="framefeed_index"),
    url(r'^page(?P<page_num>\d+)/$', views.index, name="framefeed_page"),
    url(r'^(?P<slug>[-\w]+)-(?P<id>\d+)/$', views.post, name="framefeed_post"),
    (r'^feed/(?P<url>.*)/$', 'django.contrib.syndication.views.feed', {'feed_dict': feeds}),
)
