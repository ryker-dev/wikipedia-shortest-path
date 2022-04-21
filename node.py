from socketserver import ThreadingMixIn
from xmlrpc.server import SimpleXMLRPCServer
import wikipediaapi

IP = ("localhost", 3000)
wiki = wikipediaapi.Wikipedia('en')

class SimpleThreadedXMLRPCServer(ThreadingMixIn, SimpleXMLRPCServer):
    pass

server = SimpleThreadedXMLRPCServer(IP)

class function_class:

    def search(self, dest, *args):
        last = args[0] or ""
        res = None
        links = wiki.page(dest).links

        for title in sorted(links.keys()):
            if (title == dest):
                return title
        return links.items()

#### Register functions
server.register_instance(function_class())
####

if __name__ == '__main__':
    try:
        print("Starting server")
        server.serve_forever()
    except KeyboardInterrupt:
        print("Shutting down server")