from json import dumps
import sys
from apps.hello import models


class WebRequestMiddleware(object):
    def process_view(self, request, view_func, view_args, view_kwargs):
        setattr(request, 'hide_post', view_kwargs.pop('hide_post', False))

    def process_response(self, request, response):

        if request.path.endswith('/favicon.ico') or \
           request.path.endswith('/get_requests/'):
            return response

        try:
            self.save(request, response)
        except Exception as e:
            print(e, end="Error saving request log")

        return response

    def save(self, request, response):
        models.WebRequest(
            host=request.get_host(),
            path=request.path,
            method=request.method,
            uri=request.build_absolute_uri(),
            status_code=response.status_code,
            get=None if not request.GET else dumps(request.GET),
            post=None if (not request.POST) else dumps(request.POST),
            is_secure=request.is_secure(),
            is_ajax=request.is_ajax(),
        ).save()
