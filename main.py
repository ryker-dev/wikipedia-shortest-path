import wikipediaapi

wiki = wikipediaapi.Wikipedia('en')

def search(page, name, *args):
    links = page.links

    for title in sorted(links.keys()):
        print(title)
        page = wiki.page(title)
        links.update(page.links)
    
    return links

def main():
    results = {}
    wiki = wikipediaapi.Wikipedia('en')
    page = wiki.page('Python_(programming_language)')
    results.update(search(page, "cock"))
    print(results)

if __name__ == '__main__':
    main()