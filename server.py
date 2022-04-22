from xmlrpc.client import Server, ServerProxy
import wikipedia

ADDRESS = "http://localhost:3000"
proxy = ServerProxy(ADDRESS, allow_none=True)

NODES = {
        '1': ("localhost", 3000),
        '2': ("localhost", 3001),
}
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

''' def check_parameters(start, dest):
        for p in [start, dest]:
                try:
                        ret = wikipedia.search(p)
                        if (ret == None):
                                print(F"Could not find any pages matching {p}")
                                return False
                        return True
                except wikipedia.exceptions.DisambiguationError as e:
                        print(f"Term {p} is not disambiguous. Try:")
                        print(e.options)
                        return False
                except wikipedia.PageError as e:
                        print(f"Could not find any pages matching {p}\n{e}")
                        return False '''


def shortest_path(start, dest):
        if (start == dest):
                return start

        ##if (not check_parameters(start, dest)): return None
        
        searched_articles = []
        articles = []

        ''' roots = proxy.search(wikipedia.search(start)[0])

        print(roots)
        for root in roots:
                que = [article(root)]
        print(que) '''

        que = []
        que.append(article(wikipedia.search(start)[0]))
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

        return None
                        
                                
                        

if __name__ == '__main__':
        path = shortest_path("Mercury", "Adolf Hitler")
        print(path)