from django.db import models
from django.conf import settings
from django.utils.translation import ugettext_lazy as _
from django.core.urlresolvers import reverse
from django.utils.safestring import mark_safe
from imagekit.models import ImageModel
from tagging.fields import TagField
from tagging.utils import parse_tag_input
from framefeed.signals import make_slug, process_exif
from framefeed.utils import root_url


photo_cache_path = getattr(settings, 'FRAMEFEED_PHOTOCACHE_PATH', 'photos')

class Meta(models.Model):
    """
    Meta key-value values for each photopost, like aperture, shutter, etc.
    """
    field = models.CharField(max_length=250)
    value = models.CharField(max_length=250)

    def __unicode__(self):
        return u"%s: %s" % (self.field, self.value)

    class Meta:
        unique_together = ['field', 'value']


class PhotoPostManager(models.Manager):
    """
    Default photo post manager.
    """
    def published(self):
        return self.filter(published=True)

class GeneralPhotoPost(ImageModel):
    """
    Main meta photo post model.
    """
    title = models.CharField(blank=True, max_length=250)
    slug = models.SlugField()
    original_image = models.ImageField(upload_to=photo_cache_path)
    text = models.TextField(blank=True)
    tags = TagField()
    meta = models.ManyToManyField(Meta, blank=True)
    published = models.BooleanField(default=False)
    updated_at = models.DateTimeField(auto_now=True)
    publish_at = models.DateTimeField(auto_now_add=True)

    objects = PhotoPostManager()

    def __unicode__(self):
        return self.title or unicode(self.original_image)

    def get_tags_list(self):
        return parse_tag_input(self.tags)

    def get_feed_title(self):
        return self.title

    def get_feed_text(self):
        return mark_safe(u"<img src='%s' alt=''/>\n<br/><p>%s</p>" % (root_url() + self.medium_img.url, self.text))

    class Meta:
        abstract = True
        ordering = ['-publish_at',]
        get_latest_by = 'publish_at'

    class IKOptions:
        """
        Default ImageKit option, may be set via django settings
        """
        spec_module = getattr(settings, 'FRAMEFEED_SPECS', 'framefeed.imagekit_opts')
        cache_dir = photo_cache_path
        image_field = 'original_image'


if getattr(settings, 'FRAMEFEED_MODEL', False): # in case you use custom inherited model
    try:
        default_model = __import__(settings.FRAMEFEED_MODEL,  {}, {}, [''])
    except ImportError:
        raise ImportError('Unable to load framefeed model: %s' % settings.FRAMEFEED_MODEL)
    if not issubclass(default_model, GeneralPhotoPost):
        raise ImportError('The class %s is not subclass of GeneralPhotoPost' % settings.FRAMEFEED_MODEL)
else: # use default model
    class PhotoPost(GeneralPhotoPost):
        pass
    default_model = PhotoPost

# create meta fields from exif if not disabled in settings
if getattr(settings, 'FRAMEFEED_PROCESS_EXIF', True):
    models.signals.post_save.connect(process_exif, default_model)
# generate slug if empty
models.signals.pre_save.connect(make_slug, default_model)
