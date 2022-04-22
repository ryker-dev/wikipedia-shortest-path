from asyncio import exceptions
from itertools import count
from xmlrpc.client import Server, ServerProxy
import wikipedia
import threading
import concurrent.futures
import numpy as np

ADDRESS = "http://localhost:3000"

NODES = {
        '0': ("localhost", 3000),
        '1': ("localhost", 3001),
        '2': ("localhost", 3002),
        '3': ("localhost", 3003),
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

def distribution_thread(node, chunks, que, searched_articles):
        proxy = ServerProxy(f"http://{node[0]}:{node[1]}", allow_none=True)
        ''' for i in range(0, len(que)):
                if (i % int(nodenum) == 0):
                        to_search.append(que[i]) '''
        results = [];

        print(f"I WAS GIVEN A CHUNK OF LENGTH {len(chunks)}")
        while len(chunks) > 0:
                for page in chunks:
                        ## Add threading
                        links = proxy.search(page.title)
                        ##print(to_search)
                        if (page.title in searched_articles or links == None):
                                que.remove(page)
                                continue
                        for i in links:
                                a = article(i, page)
                                que.append(a)
                                searched_articles.extend(page.title)
                                results.append(a)
                        que.remove(page)

        return results
        ''' for i in res:
                print(i)
                if (i in searched_articles or i == None): continue
                a = article(i, artic)
                if (i == dest): return get_path(a)
                que.append(a)
                searched_articles.append(i)
                que.remove(i) '''

## Jurgen Strydom, Stackoverflow, Feb 21, 2019 https://stackoverflow.com/questions/24483182/python-split-list-into-n-chunks 
def divide(que, n):
    """Yield n number of striped chunks from l."""
    for i in range(0, n):
        yield que[i::n]

def shortest_path(start, dest):
        if (start == dest):
                return start
        
        searched_articles = []

        que = []
        ret = []
        que.append(article(wikipedia.search(start)[0]))
        ''' for nodenum in NODES:
                node = NODES[nodenum]
                with concurrent.futures.ThreadPoolExecutor() as executor:
                        future = executor.submit(distribution_thread, nodenum, node, dest, que, searched_articles)
                        ret = future.result()
                que.extend(ret) '''
        
        for x in range(5):
                ## Divide labour between nodes
                chunks = []
                threads = []
                chunks = list(divide(que, len(NODES)))

                ##print(f"!!!!{chunks}")
                ''' for chunk in chunks:
                        print(len(chunk)) '''
                
                for nodenum in NODES:
                        node = NODES[nodenum]
                        try:
                                chunk = chunks[int(nodenum)]
                                if (len(chunk) < 1): continue
                                thread = threading.Thread(target=distribution_thread, args=(node, chunk, que, searched_articles))
                                threads.append(thread)
                                thread.start()
                        except IndexError:
                                continue

                for thread in threads:
                        thread.join()

        ##que = que + list(set(res) - set(que))

        return None
                        
                                
                        

if __name__ == '__main__':
        path = shortest_path("Ujjal Singh", "The Crown")