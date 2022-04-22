from inspect import trace
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

    def get_route(self, p:page):
        print(p)
        path = [p.title]
        while (p.parent != None):
            path.insert(0, p.parent.title)
            p = p.parent
        
        return path

    def search(self, start, dest):
        ## TODO: If start == dest return

        root = page(start)
        res = wikipedia.search(start)
        depth = []

        for p in res:
            n = page(p, root)
            if (p == dest):
                print(p, dest)
                print(self.get_route(n))
                return self.get_route(n)
            depth.append(page(p, n))


        ''' res = wikipedia.search(p.title)
        pages = []

        for title in res:
            if (title == p.title):
                continue
            pages.append(page(title, p))
        return pages '''

#### Register functions
server.register_instance(wikipedia_search())
####

if __name__ == '__main__':
    try:
        print("Starting server")
        server.serve_forever()
    except KeyboardInterrupt:
        print("Shutting down server")