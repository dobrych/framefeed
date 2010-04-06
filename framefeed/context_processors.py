from django.conf import settings

def settings_vars(request):
    return { 'FRAMEFEED_TITLE': getattr(settings, 'FRAMEFEED_TITLE', 'Framefeed Title'), }
