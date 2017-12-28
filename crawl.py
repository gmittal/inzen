# Inzen: Search Engine
# Written by Gautam Mittal and Daniel Zhu

from __future__ import unicode_literals
import requests, urllib2, json, html2text
from bs4 import BeautifulSoup

# Initialize constants
SEED_PAGE = 'Carnegie_Mellon_University'
SAVE_PATH = 'data/www/'

# HTML removal service
h = html2text.HTML2Text()
h.ignore_links = True
h.ignore_images = True

q = [] # Queue of articles to index

# Crawl a Wikipedia page
def crawl(u):
    if u == "None" or u == "":
        return
    print len(q), u

    # Download page
    r = requests.get('https://en.wikipedia.org/wiki/'+u).text
    parsed_html = BeautifulSoup(r, "lxml")
    text = h.handle(r).encode('utf-8')
    f = open(SAVE_PATH + u +".txt","w")
    f.write(text)
    f.close()

    # Find all linked Wikipedia pages
    for link in parsed_html.find_all('a'):
        try:
            n = str(link.get('href')).split('/')[-1].encode('utf-8').strip()
            n = urllib2.unquote(n.encode('utf-8').strip()).encode('utf8')

            if (not "." in n.decode('utf-8')):
                if (not "#" in n.decode('utf-8')):
                    if (not ":" in n.decode('utf-8')):
                        if (not "%" in n.decode('utf-8')):
                            if (not "?" in n.decode('utf-8')):
                                q.append(str(n))
        except UnicodeDecodeError:
            return
        except UnicodeEncodeError:
            return

# Download the Internet
def download():
    while len(q) > 0:
        o = q[0]
        q.pop(0)
        crawl(o)

if __name__ == "__main__":
    print "Crawling Wikipedia..."
    crawl(SEED_PAGE)
    download()
