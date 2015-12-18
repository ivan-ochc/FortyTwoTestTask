from json import dumps
from apps.hello import models


class WebRequestMiddleware(object):
    def process_response(self, request, response):

        if request.path.endswith('/favicon.ico') or \
           request.path.endswith('/get_requests/'):
            return response

        self.save(request, response)

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
