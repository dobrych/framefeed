from PIL import Image
from PIL.ExifTags import TAGS
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
    i = Image.open(instance.original_image.file)
    coded_tags = i._getexif()
    i.fp.close() # close file proxy
    tags = dict()
    # converting exif fields from numbers to text
    for tag, value in coded_tags.items():
        decoded = TAGS.get(tag, tag)
        tags[decoded] = value
    if not tags:
        return
    fnum = tags.get('FNumber')
    # calculating aperture and making it human-readable
    if len(fnum) == 2 and fnum[1] != 1: # isn't divided by 1
        aperture = u"f/%.1f" % (float(fnum[0])/float(fnum[1]))
    elif fnum[0]:
        aperture = u"f/%s" % (fnum[0])
    else:
        aperture = None
    # converting timing tuple into readable text like 1/60
    timing = tags.get('ExposureTime')
    if len(timing) == 2 and timing[1] != 1: # less then second
        exposure = u"/".join([str(i) for i in timing])
    elif timing[0]:
        exposure = u"%s sec" % (timing[0])
    else:
        exposure = None
    # converting focal length tuple to readable text
    focal = tags.get('FocalLength')
    if len(focal) == 2:
        focal = "%smm" % (int(focal[0]/focal[1]))
    elif len(focal) == 1:
        focal = "%smm" % (focal[0])
    else:
        focal = None
    Meta = instance.meta.model
    # updating db
    ma, res = Meta.objects.get_or_create(field='Aperture', value=aperture)
    ms, res = Meta.objects.get_or_create(field='Shutter', value=exposure)
    mf, res = Meta.objects.get_or_create(field='Focal length', value=focal)
    instance.meta.add(ma,ms,mf)
