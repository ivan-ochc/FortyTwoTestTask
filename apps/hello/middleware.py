from json import dumps
from apps.hello import models


class WebRequestMiddleware(object):

    def process_response(self, request, response):

        priority = 1

        if request.path.endswith('/favicon.ico') or \
           request.path.endswith('/get_requests/'):
            return response

        if request.path.startswith('/admin/'):
            priority = 0

        self.save(request, response, priority)

        return response

    def save(self, request, response, priority):
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
            priority=priority
        ).save()
