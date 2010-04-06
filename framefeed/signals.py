import EXIF
from django.utils.translation import ugettext_lazy as _
from framefeed.utils import make_hash


def make_slug(sender, instance, **kwargs):
    """
    Set slug from title or random hash as slug for unnamed items.
    """
    if not instance.slug:
        if hasattr(instance, 'title') and instance.title:
            instance.slug = slugify(instance.title)
        else:
            instance.slug = make_hash()

def process_exif(sender, instance, **kwargs):
    """
    Create Meta key-value pairs from exif data.
    """
    tags = EXIF.process_file(instance.original_image.file)
    if not tags:
        return
    fnum = unicode(tags.get('EXIF FNumber')).split('/')
    # calculate aperture
    if len(fnum) == 2:
        aperture = u"f/%.1f" % (float(fnum[0])/float(fnum[1]))
    elif fnum[0] != 'None':
        aperture = u"f/%s" % (fnum[0])
    else:
        aperture = None
    exposure = unicode(tags.get('EXIF ExposureTime'))
    focal = tags.get('EXIF FocalLength')
    if focal: # prettify focal length value
        focal = "%smm" % (str(focal))
    Meta = instance.meta.model
    ma, res = Meta.objects.get_or_create(field='Aperture', value=aperture)
    ms, res = Meta.objects.get_or_create(field='Shutter', value=exposure)
    mf, res = Meta.objects.get_or_create(field='Focal length', value=focal)
    instance.meta.add(ma,ms,mf)
    print instance.meta.all()
