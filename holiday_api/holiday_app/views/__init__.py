from django.views.decorators.csrf import ensure_csrf_cookie
from django.views.generic.base import TemplateView
from django.utils.decorators import method_decorator
from django.shortcuts import render
from django.template.exceptions import TemplateDoesNotExist
from django.http import Http404


class IndexView(TemplateView):
    """
    The template viewer.
    """

    template_name = 'index.html'

    @method_decorator(ensure_csrf_cookie)
    def get(self, request, *args, **kwargs):
        request_path = request.path[1:]
        if len(request_path) == 0:
            request_path = 'index.html'

        try:
            return render(request, request_path, {})
        except TemplateDoesNotExist:
            raise Http404('404 Not Found')
