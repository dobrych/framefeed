from django.conf import settings
from framefeed.utils import root_url


def settings_vars(request):
    return { 'FRAMEFEED_TITLE': getattr(settings, 'FRAMEFEED_TITLE', 'Framefeed Title'), }

def cur_site(request):
    return {'FRAMEFEED_ROOT_URL': root_url()}
