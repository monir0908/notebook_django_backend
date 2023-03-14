import json
import logging
from json import JSONDecodeError
from urllib.parse import parse_qs
from django.http import JsonResponse, HttpResponse
from django.core.exceptions import SuspiciousOperation, RequestDataTooBig
logger = logging.getLogger(__name__)


class RequestResponseLogMiddleware:
    def __init__(self, get_response):
        self.get_response = get_response

    def __call__(self, request):
        data = {
            'method': request.method,
            'headers': dict(request.headers),
            'query_params': dict(request.GET),
        }
        path = str(request.get_full_path()).replace('/api/v3/', '').replace('/', '-').upper()
        data['requested_endpoint'] = path
        # if hasattr(request, 'body') and request.body:
        #     try:
        #         data['request_body'] = json.loads(request.body.decode('utf-8'))
        #     except JSONDecodeError:
        #         data['request_body'] = parse_qs(request.body.decode('utf-8'))
        if hasattr(request, 'body') and request.body:
            try:
                data['request_body'] = json.loads(request.body.decode('iso-8859-1'))
            except JSONDecodeError:
                data['request_body'] = parse_qs(request.body.decode('iso-8859-1'))

        response = self.get_response(request)
        if hasattr(response, 'data'):
            data['response_body'] = response.data
        data['status'] = response.status_code
        if data['status'] // 100 == 5:
            logger.error(json.dumps(data))
        else:
            logger.info(json.dumps(data))
        return response
    
    # def process_exception(self, request, exception):
    #     print('middleware process exeption', exception)
    #     if isinstance(exception, RequestDataTooBig):
    #         print('CALLED')
    #         return HttpResponse("dummy", content_type="text/plain")
    #         #return JsonResponse({"error":"file is too big"})