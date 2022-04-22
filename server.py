from xmlrpc.client import Server, ServerProxy

ADDRESS = "http://localhost:3000"
proxy = ServerProxy(ADDRESS, allow_none=True)

class page:
    def __init__(self, title, parent=None):
        self.title = title
        self.parent = parent

def create_page(title, parent):
        return page(title, parent)

def shortest_path(start, dest):
        if (start == dest):
                return start

        root = page(start)
        res = proxy.search(root)
        depth = []
        nextDepth = []

        ''' while True:
                for p in res:
                        _page = create_page(p["title"], p["parent"])
                        depth.append(_page)
                        if (p["title"] == dest):
                                break '''
                        ##print(f'Searching {p}...')
                        ##nextDepth.extend([proxy.search(p["title"])])
        
                ##depth = nextDepth
                ##break;
        ''' path = []
        while (_page.parent != start):
                path.insert(0, _page.parent.title)
                _page = _page.parent '''
        
        print(res)

if __name__ == '__main__':
        shortest_path("Germany", "East Germany")