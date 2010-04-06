from django.conf import settings
from django.http import Http404
from django.core.paginator import Paginator
from django.template.context import RequestContext
from django.shortcuts import get_object_or_404, render_to_response, redirect
from framefeed.models import default_model


default_template = getattr(settings, 'FRAMEFEED_LAYOUT', 'framefeed.html')
index_page_limit = getattr(settings, 'FRAMEFEED_PAGINATE_BY', False)

def index(request, template=default_template, model=default_model, page_num=None):
    """
    Show index page with list of photo-posts.
    """
    if index_page_limit:
        p = Paginator(model.objects.published(), index_page_limit)
        page = p.page(page_num or 1)
        objects = page.object_list
    else:
        p, page = None, None
        objects = model.objects.published()
    return render_to_response(default_template,
                              {'paginator': page, 'object_list': objects},
                               RequestContext(request))

def post(request, slug, id, template=default_template, model=default_model):
    """
    Show individual photo-post.
    """
    try:
        p = model.objects.published().get(pk=id, slug=slug)
    except model.DoesNotExist:
        raise Http404
    return render_to_response(default_template, {'object': p}, RequestContext(request))
