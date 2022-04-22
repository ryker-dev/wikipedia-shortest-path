from xmlrpc.client import Server, ServerProxy

ADDRESS = "http://localhost:3000"
proxy = ServerProxy(ADDRESS, allow_none=True)

class page:
    
    def __init__(self, title, parent):
        self.title = title
        self.parent = parent

def shortest_path(start, dest):
        if (start == dest):
                return start

        depth = proxy.search(start);
        nextDepth = []

        while True:
                for p in depth:
                        print(f'Searching {p}...')
                        nextDepth.extend([proxy.search(p["title"])])
        
                depth = nextDepth
                break;

if __name__ == '__main__':
        shortest_path("Germany", "East Germany")