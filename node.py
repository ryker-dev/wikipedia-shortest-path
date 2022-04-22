from mimetypes import init
from socketserver import ThreadingMixIn
from xmlrpc.server import SimpleXMLRPCServer
import wikipedia
import sys

IP = (sys.argv[1], int(sys.argv[2]))

class SimpleThreadedXMLRPCServer(ThreadingMixIn, SimpleXMLRPCServer):
    pass

server = SimpleThreadedXMLRPCServer(IP, allow_none=True, logRequests=False)

class wikipedia_search:

    def search(self, title):
        try:
            print(f"Searching {title}")
            pages = wikipedia.page(title).links
            print(f"Found {len(pages)} links from {title}")
            return pages
        except (wikipedia.DisambiguationError) as e:
            print(f"{e}")
            return e.options
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