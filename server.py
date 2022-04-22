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

        res = proxy.search(start, dest)
        
        print(res)

if __name__ == '__main__':
        shortest_path("Germany", "East Germany")