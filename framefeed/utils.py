import uuid
import base64
import random
from django import VERSION
from django.contrib.sites.models import Site


def make_hash(lenght=7):
    """
    Creates random hash (youtube-like) with specified lenght
    """
    bstr = base64.b64encode("%s" % uuid.uuid4())
    start_p = random.randrange(1, len(bstr) - lenght)
    return bstr[start_p:start_p+lenght]

def django_is_lower_1_2():
    if VERSION[0] == 1 and VERSION[1] < 2:
        return True
    elif VERSION[0] >= 1:
        return False
    return True

def root_url():
    return 'http://%s' % (Site.objects.get_current().domain)
