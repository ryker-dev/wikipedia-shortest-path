from mimetypes import init
from socketserver import ThreadingMixIn
from xmlrpc.server import SimpleXMLRPCServer
import wikipedia

IP = ("localhost", 3000)

class SimpleThreadedXMLRPCServer(ThreadingMixIn, SimpleXMLRPCServer):
    pass

server = SimpleThreadedXMLRPCServer(IP, allow_none=True)

class wikipedia_search:

    def search(self, title):
        try:
            print(f"Searching {title}")
            pages = wikipedia.page(title).links
            return pages
        except (wikipedia.DisambiguationError) as e:
            ret = []
            for page in e.options: ret.append(self.search(page))
            return ret
        except (wikipedia.PageError) as e:
            print(f"Searching page {title} failed!\n{e}")
        return None

#### Register functions
server.register_instance(wikipedia_search())
####

if __name__ == '__main__':
    try:
        print("Starting server")
        server.serve_forever()
    except KeyboardInterrupt:
        print("Shutting down server")