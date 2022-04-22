from xmlrpc.client import Server, ServerProxy
import threading
import sys

ADDRESS = "http://localhost:3000"

## Edit available nodes here
## (address, port)
NODES = {
        '0': ("localhost", 3000),
        '1': ("localhost", 3001),
        '2': ("localhost", 3002),
        '3': ("localhost", 3003),
}

########

class article:
        """Used to store the retreived pages in a tree structure"""
        def __init__(self, title, parent=None):
                self.title = title
                self.parent = parent

def get_path(a:article):
        """Retreives the path up to the highest parent. Returns a list of strings."""
        path = []
        while a != None:
                path.insert(0, a.title)
                a = a.parent

        return path

def print_path(path):
        """Takes a list of strings and prints them in the result format."""
        res = ""
        for i in range(len(path)-1):
                res = res + f"{path[i]} -> "
        res = res + f"{path[i+1]}"
        return res

def distribution_thread(node, chunks, queue, searched_articles):
        proxy = ServerProxy(f"http://{node[0]}:{node[1]}", allow_none=True)
        results = [];

        for page in chunks:
                ## Add threading
                links = proxy.search(page.title)
                ##print(to_search)
                if (page.title in searched_articles or links == None):
                        queue.remove(page)
                        continue
                for i in links:
                        a = article(i, page)
                        queue.append(a)
                        searched_articles.append(i)
                        results.append(a)
                queue.remove(page)

        return results

## Jurgen Strydom, Stackoverflow, Feb 21, 2019 https://stackoverflow.com/questions/24483182/python-split-list-into-n-chunks 
def divide(queue, n):
    """Yield n number of striped chunks from l."""
    for i in range(0, n):
        yield queue[i::n]

def shortest_path(start, dest):
        """Main function to start the retreival of the shortest path and call the nodes."""
        if (start == dest):
                return start
        
        searched_articles = []

        root = article(start.lower())
        queue = [root]
        ret = []
        ##queue.append(article(wikipedia.search(start)[0]))
        
        while True:
                ## Divide labour between nodes
                chunks = []
                threads = []
                found_article = article(None)
                chunks = list(divide(queue, len(NODES)))
                
                print(f"Calling remote nodes called with {len(queue)} page(s).")
                counter = 0
                for nodenum in NODES:
                        node = NODES[nodenum]
                        try:
                                chunk = chunks[int(nodenum)]
                                if (len(chunk) < 1): continue
                                thread = threading.Thread(target=distribution_thread, args=(node, chunk, queue, searched_articles))
                                threads.append(thread)
                                thread.start()
                                counter += 1
                        except IndexError:
                                continue
                
                print(f"{counter} remote node(s) called.")
                print(f"waiting...")

                for thread in threads:
                        thread.join()

                if (not queue or len(queue) < 1):
                        print("Couldn't find a path between the two articles.")
                        break
                if (dest in searched_articles):
                        for page in queue:
                                if page.title == dest:
                                        return get_path(page)

        ##queue = queue + list(set(res) - set(queue))

        return None
                        
                                
                        

if __name__ == '__main__':
        path = shortest_path("Germany", "Finland")
        if (path): print(print_path(path))