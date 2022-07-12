"""
Very simple HTTP server in python for logging requests
Usage::
    ./server.py [<port>]
"""

from bson.json_util import dumps, loads
from http.server import BaseHTTPRequestHandler, HTTPServer
import logging

from context import dao
from dao.dao_db_users import DAO_db_users
from dao.dao_db_community import DAO_db_community


class Handler(BaseHTTPRequestHandler):

    def _set_response(self, code, dataType='text/html'):
        self.send_response(code)
        self.send_header('Content-type', dataType)
        self.end_headers()

    def do_GET(self):
        """
        self.path == /all -> devolver todos los ficheros
        self.path != /all -> devolver el fichero que tenga el nombre igual a 'self.path[1:]'
        """
        logging.info("GET request,\nPath: %s\nHeaders:\n%s\n", str(self.path), str(self.headers))

        request = str(self.path[1:])
        daoCommunity = DAO_db_community("localhost", 27018, "spice", "spicepassword")
        if request == "all":
            data = daoCommunity.getFileLists()
            self._set_response(200, 'application/json')
            self.wfile.write(dumps(data).encode(encoding='utf_8'))
        else:
            data = daoCommunity.getFileList(request)
            if data != []:
                self._set_response(200, 'application/json')
                self.wfile.write(dumps(data).encode(encoding='utf_8'))
            else:
                self._set_response(404)
                self.wfile.write("GET request for {}".format(self.path).encode('utf-8'))

    def do_POST(self):
        content_length = int(self.headers['Content-Length'])  # <--- Gets the size of data
        post_data = self.rfile.read(content_length)  # <--- Gets the data itself
        logging.info("POST request,\nPath: %s\nHeaders:\n%s\n\nBody:\n%s\n",
                     str(self.path), str(self.headers), post_data.decode('utf-8'))

        user = loads(post_data.decode('utf-8'))
        daoUsers = DAO_db_users("localhost", 27018, "spice", "spicepassword")
        ok = daoUsers.insertUser_API(user)
        if ok:
            self._set_response(204)
            self.wfile.write("POST request for {}".format(self.path).encode('utf-8'))
            # <Update Community Model>
            # TODO: Hacer Llamada al Community Model
            # </Update Community Model>

        else:
            self._set_response(500)
            self.wfile.write("POST request for {}".format(self.path).encode('utf-8'))


def run(server_class=HTTPServer, handler_class=Handler, port=8090):
    logging.basicConfig(level=logging.INFO)
    server_address = ('localhost', port)
    httpd = server_class(server_address, handler_class)
    logging.info('Starting httpd...\n')
    try:
        httpd.serve_forever()
    except KeyboardInterrupt:
        pass
    httpd.server_close()
    logging.info('Stopping httpd...\n')


if __name__ == '__main__':
    from sys import argv

    if len(argv) == 2:
        run(port=int(argv[1]))
    else:
        run()
