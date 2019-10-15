import json

from tornado import web, escape
from const import HTTP_CODES


class RequestHandler(web.RequestHandler):
    """Basic request handler.

    Attributes:
        `methods` (:list): allowed methods
        `session` (:Any): session object
        `logging` (:Any): logger object
    """
    methods = ['GET', 'POST', 'PUT', 'DELETE', 'PATCH']
    session = None
    logging = None

    def initialize(self):
        if self.settings.get('logging'):
            self.logging = self.settings.get('logging')

    # def set_default_headers(self) -> None:
    #     if self.application.settings.get('service_debug', True):
    #         self.set_header("Access-Control-Allow-Origin", "*")
    #         _ = 'Content-Type, Depth, User-Agent, X-File-Size, ' \
    #             'X-Requested-With, X-Requested-By, If-Modified-Since, ' \
    #             'X-File-Name, Cache-Control, Authorization'
    #         self.set_header("Access-Control-Allow-Headers", _)
    #         _ = 'POST, GET, PUT, DELETE, OPTIONS, PATCH'
    #         self.set_header('Access-Control-Allow-Methods', _)
    #         self.set_header('Access-Control-Allow-Credentials', 'true')

    def get_all_arguments(self):
        try:
            json_data = escape.json_decode(self.request.body)
        except (json.JSONDecodeError, UnicodeDecodeError):
            json_data = {}

        if json_data:
            return json_data.keys()
        else:
            return self.request.arguments

    def get_argument(self, name: str, default=None, strip: bool = True) -> str:
        try:
            json_data = escape.json_decode(self.request.body)
        except (json.JSONDecodeError, UnicodeDecodeError):
            json_data = {}

        if json_data.get(name):
            return json_data.get(name)
        elif super(RequestHandler, self).get_argument(name, None):
            return super(RequestHandler, self).get_argument(name)
        elif default:
            return default

    def finish_with_error(self, code, title=None, detail=None, fields=None):
        if not title:
            title = HTTP_CODES.get(code, 'Unknown error')

        message = {
            'title': title,
            'status': code,
            'instance': self.request.path,
        }

        if detail:
            message['detail'] = detail
        if fields:
            message['fields'] = fields

        self.set_header('Content-type', 'application/problem+json')
        self.set_status(code)
        self.finish(message)

    def get(self, *args, **kwargs):
        return self.finish_with_error(code=405)

    def post(self, *args, **kwargs):
        return self.finish_with_error(code=405)
