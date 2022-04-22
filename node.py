from mimetypes import init
from socketserver import ThreadingMixIn
from xmlrpc.server import SimpleXMLRPCServer
import wikipedia
import wikipediaapi
import sys

IP = (sys.argv[1], int(sys.argv[2]))

class SimpleThreadedXMLRPCServer(ThreadingMixIn, SimpleXMLRPCServer):
    pass

server = SimpleThreadedXMLRPCServer(IP, allow_none=True, logRequests=False)

class wikipedia_search:
    
    def get_links(self, title):
        """For use with Wikipedia-API"""
        wiki = wikipediaapi.Wikipedia('en')
        ret = []
        links = wiki.page(title).links
        for title in sorted(links.keys()):
            print(title)
            ret.append(title)
        return ret

    def search(self, title):
        """Searches for wikipedia pages with title and returns a list of links on the page"""
        try:
            print(f"Searching {title}")

            pages = wikipedia.page(title.lower().replace(" ", ""), auto_suggest=False).links
            ##pages = self.get_links(title)

            print(f"Found {len(pages)} links from {title}")
            print(pages)
            return pages
        except (wikipedia.DisambiguationError) as e:
            print(f"{e}")
            return None
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