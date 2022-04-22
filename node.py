from mimetypes import init
from socketserver import ThreadingMixIn
from xmlrpc.server import SimpleXMLRPCServer
import wikipedia

IP = ("localhost", 3000)

class page:
    def __init__(self, title, parent=None):
        self.title = title
        self.parent = parent


class SimpleThreadedXMLRPCServer(ThreadingMixIn, SimpleXMLRPCServer):
    pass

server = SimpleThreadedXMLRPCServer(IP)

class wikipedia_search:

    def search(self, p:page) -> list[page]:
        print(type(p))
        print(p)
        res = wikipedia.search(p.title)
        pages = []

        for title in res:
            if (title == p.title):
                continue
            pages.append(page(title, p))
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