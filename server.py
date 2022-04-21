from xmlrpc.client import Server, ServerProxy

ADDRESS = "http://localhost:3000"
proxy = ServerProxy(ADDRESS, allow_none=True)

if __name__ == '__main__':
        results = proxy.search("Germany")
        print(results)