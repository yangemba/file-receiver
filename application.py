import logging
import os
import re

from tornado import web, options, ioloop
from base_handler import RequestHandler


class TornadoApplication(web.Application):
    config = {}
    working_directory = ''
    db_settings = {}
    logging = None

    def __init__(self, **kwargs):
        if not kwargs.get('urls'):
            raise ValueError('You need to provide "urls" variable to init TornadoApplication')

        urls = kwargs.get('urls')
        if not isinstance(urls, list):
            raise TypeError('Variable "urls" must be a list')
        if not isinstance(urls[0], dict):
            raise TypeError('Items in "urls" must be a dictionaries')

        self.io_loop = ioloop.IOLoop.instance()
        if not self.config:
            self.setup_config(kwargs.get('config_file', 'service.conf'))
        url_prefix = self.config.get('service_url_prefix', '')

        queues = kwargs.get('queues', [])
        uuid_regexp = '([0-9a-f]{8}-[0-9a-f]{4}-4[0-9a-f]{3}-[89ab][0-9a-f]{3}-[0-9a-f]{12})'

        handlers = []
        for url in urls:
            url_regexp = f'{url_prefix}/{url.get("url").format(uuid=uuid_regexp)}/?'
            handlers.append(
                web.url(
                    re.compile(url_regexp),
                    url.get("handler")
                )
            )

    def start_io_loop(self):
        self.io_loop.start()

    def setup_working_directory(self):
        self.working_directory = os.path.dirname(os.path.realpath(__file__)) + '/../'

    def setup_config(self, additional_options=(), config_file='service.conf'):
        self.setup_working_directory()
        self.logging = setup_logging()

        options.define('service_url_prefix', '/', str, 'Url prefix for service')
        options.define('service_host', '0.0.0.0', str, 'Service host')
        options.define('service_port', 21000, int, 'Service port')
        options.define('service_debug', True, bool, 'Auto-reload service on changes')
        options.define('service_version', '1.0.0', str, 'Service version')
        options.define('service_name', 'Service', str, 'Service name')
        options.define('service_description', 'Service description', str, 'Service description')

        options.define('postgresql_host', 'localhost', str, 'Database host')
        options.define('postgresql_port', 5432, int, 'Database port')
        options.define('postgresql_name', 'service', str, 'Database name')
        options.define('postgresql_user', 'user', str, 'Database user')
        options.define('postgresql_pass', 'password', str, 'Database password')

        options.define('smtp_host', 'localhost', str, 'SMTP host')
        options.define('smtp_port', 25, int, 'SMTP port')
        options.define('smtp_tls', False, bool, 'Use TSL')
        options.define('smtp_user', '', str, 'SMTP auth user')
        options.define('smtp_password', '', str, 'SMTP auth password')
        options.define('smtp_name', '', str, 'Mail sender name')
        options.define('smtp_email', '', str, 'Mail sender email')

        options.define('log_filename', 'logs/service.log', str, 'Log file path and name')

        options.define('swagger_enabled', True, bool, 'Enable swagger documentation')
        options.define('swagger_service_auth', False, bool, 'Enable swagger auth')
        options.define('swagger_url', '/docs', str, 'Swagger docs postfix')
