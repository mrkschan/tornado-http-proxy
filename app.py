import logging
import os

from tornado.log import enable_pretty_logging
from tornado.ioloop import IOLoop
from tornado.options import define, parse_command_line, options
from tornado.web import Application, RequestHandler, HTTPError, url

import requests


class ProxyHandler(RequestHandler):
    def initialize(self):
        self.logger = logging.getLogger('tornado.general')

    def get(self, url):
        # Ignore non-proxy requests.
        if not url.startswith('http://'):
            raise HTTPError(404)

        r = requests.get(url)

        status = r.status_code
        contenttype = r.headers['content-type']

        self.set_status(status)
        self.set_header('Content-Type', contenttype)
        self.write(r.text)


def make_app(**settings):
    urls = (
        url(r'(.+)', ProxyHandler),
    )

    return Application(urls, **settings)


if __name__ == '__main__':
    enable_pretty_logging()

    define('debug', default=int(os.environ.get('DEBUG', 0)), type=int)
    define('port', default=int(os.environ.get('PORT', 8123)), type=int)

    parse_command_line()
    port = options.port
    debug = (options.debug == 1)

    app = make_app(debug=debug)
    app.listen(port)

    logger = logging.getLogger('tornado.general')
    logger.info('Listening on PORT: %d', port)

    IOLoop.current().start()
