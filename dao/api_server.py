"""
Very simple HTTP server in python for logging requests
Usage::
    ./server.py [<port>]
"""
import pymongo
from bson.json_util import dumps, loads
from http.server import BaseHTTPRequestHandler, HTTPServer
import logging

from context import dao
from dao.dao_db_perspectives import DAO_db_perspectives
from dao.dao_db_users import DAO_db_users
from dao.dao_db_communities import DAO_db_community


class Handler(BaseHTTPRequestHandler):

    # TODO:
    # + timeout
    # - incorrect path or filename

    def do_GET(self):
        """
        _get handler_
        API:
        /file/all                       -> return all files
        /file/{fileId}                  -> return file with name equal to 'self.path[1:]'
        /perspective/all                -> ...
        /perspective/{perspectiveId}    -> ...
        /index                          -> return json files index (returns only files id)
        """
        logging.info("GET request,\nPath: %s\nHeaders:\n%s\n", str(self.path), str(self.headers))
        try:
            request = self.path.split("/")
            print("Request: ", request)
            first_arg = request[1]
            if "file" == first_arg:
                self.__getFile(request[2])
            elif "perspective" == first_arg:
                self.__getPerspertive(request[2])
            elif "index" == first_arg:
                self.__getIndex()
            else:
                print("-Error-")
                self.__set_response(404)
                self.wfile.write("-Error-\nGET request not defined.\nGET request for {}".format(self.path).encode('utf-8'))
        except Exception as e:
            print(e)
            if str(e) != "pymongo.errors.ServerSelectionTimeoutError":
                self.__set_response(500)
                self.wfile.write("-Error-\nGET request for {}".format(self.path).encode('utf-8'))
                # raise
            else:
                self.__set_response(500)
                self.wfile.write(
                    "-MongoDB connection timeout error-\nGET request for {}".format(self.path).encode('utf-8'))

    def do_POST(self):
        """
        _post handler_

        """
        content_length = int(self.headers['Content-Length'])  # <--- Gets the size of data
        post_data = self.rfile.read(content_length)  # <--- Gets the data itself
        logging.info("POST request,\nPath: %s\nHeaders:\n%s\n\nBody:\n%s\n",
                     str(self.path), str(self.headers), post_data.decode('utf-8'))

        user = loads(post_data.decode('utf-8'))
        daoUsers = DAO_db_users("localhost", 27018, "spice", "spicepassword")
        ok = daoUsers.insertUser_API(user)
        if ok:
            self.__set_response(204)
            self.wfile.write("POST request for {}".format(self.path).encode('utf-8'))
            # <Update Community Model>
            # TODO: Hacer Llamada al Community Model
            # </Update Community Model>

        else:
            self.__set_response(500)
            self.wfile.write("POST request for {}".format(self.path).encode('utf-8'))

    def __set_response(self, code, dataType='text/html'):
        self.send_response(code)
        self.send_header('Content-type', dataType)
        self.end_headers()

    def __getIndex(self):
        dao = DAO_db_community("localhost", 27018, "spice", "spicepassword")
        data = dao.getFileIndex()
        print(data)
        self.__set_response(200, 'application/json')
        self.wfile.write(dumps(data).encode(encoding='utf_8'))

    def __getPerspertive(self, perspectiveId):
        dao = DAO_db_perspectives("localhost", 27018, "spice", "spicepassword")
        if perspectiveId == "all":
            data = dao.getPerspectives()
            self.__set_response(200, 'application/json')
            self.wfile.write(dumps(data).encode(encoding='utf_8'))
        else:
            data = dao.getPerspective(perspectiveId)
            if data:
                self.__set_response(200, 'application/json')
                self.wfile.write(dumps(data).encode(encoding='utf_8'))
            else:
                self.__set_response(404)
                self.wfile.write("File not found\nGET request for {}".format(self.path).encode('utf-8'))

    def __getFile(self, fileId):
        dao = DAO_db_community("localhost", 27018, "spice", "spicepassword")
        if fileId == "all":
            data = dao.getFileLists()
            self.__set_response(200, 'application/json')
            self.wfile.write(dumps(data).encode(encoding='utf_8'))
        else:
            data = dao.getFileList(fileId)
            if data:
                self.__set_response(200, 'application/json')
                self.wfile.write(dumps(data).encode(encoding='utf_8'))
            else:
                self.__set_response(404)
                self.wfile.write("File not found\nGET request for {}".format(self.path).encode('utf-8'))


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
