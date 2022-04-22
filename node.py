from mimetypes import init
from socketserver import ThreadingMixIn
from xmlrpc.server import SimpleXMLRPCServer
import wikipedia

IP = ("localhost", 3000)

class page:

    def __init__(self, title, parent):
        self.title = title
        self.parent = parent


class SimpleThreadedXMLRPCServer(ThreadingMixIn, SimpleXMLRPCServer):
    pass

server = SimpleThreadedXMLRPCServer(IP)

class wikipedia_search:

    def search(self, name) -> list:
        res = wikipedia.search(name)
        pages = []

        for title in res:
            if (title == name):
                continue
            pages.append(page(title, name))
        return pages

#### Register functions
server.register_instance(wikipedia_search())
####

if __name__ == '__main__':
    try:
        print("Starting server")
        server.serve_forever()
    except KeyboardInterrupt:
        print("Shutting down server")