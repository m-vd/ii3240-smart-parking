# http.py

import json
from nameko.web.handlers import http

class HttpService:
    name = "http_service"

    @http('GET', '/api')
    def get_method(self, request):
        return json.dumps({ 'messages': 'welcome to our API, powered by python' })
