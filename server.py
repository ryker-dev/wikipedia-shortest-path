from xmlrpc.client import Server, ServerProxy
import wikipedia

ADDRESS = "http://localhost:3000"
proxy = ServerProxy(ADDRESS, allow_none=True)

class article:
    def __init__(self, title, parent=None):
        self.title = title
        self.parent = parent

def get_path(a:article):
        path = []
        while a != None:
                path.insert(0, a.title)
                a = a.parent

        return path

def shortest_path(start, dest):
        if (start == dest):
                return start

        searched_articles = []
        articles = []

        if (proxy.search(start) == None):
                print(f"Could not find article {start}!")
        
        if (proxy.search(dest) == None):
                print(f"Could not find article {dest}!")

        root = article(start)
        que = [root]
        while True:
                for artic in que:
                        ## Add threading
                        res = proxy.search(artic.title)
                        if (res == None): continue
                        for i in res:
                                print(i)
                                if (i in searched_articles or i == None): continue
                                a = article(i, artic)
                                if (i == dest): return get_path(a)
                                que.append(a)
                                searched_articles.append(i)

        print(articles[0].parent)

        return None
                        
                                
                        

if __name__ == '__main__':
        path = shortest_path("Mercury", "Earth")
        print(path)