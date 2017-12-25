from __future__ import unicode_literals
import requests, urllib2, json
from bs4 import BeautifulSoup
import html2text
h = html2text.HTML2Text()
h.ignore_links = True
h.ignore_images = True

q = []

def crawl(u):
    if not u == None:
        print u
    r = requests.get('https://en.wikipedia.org/wiki/'+u).text
    parsed_html = BeautifulSoup(r, "lxml")
    text = h.handle(r).encode('utf-8')
    f = open("data/www/"+ u +".txt","w")
    f.write(text)
    f.close()
    
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

def dl():
    while len(q) > 0:
        o = q[0]
        q.pop(0)
        crawl(o)

if __name__ == "__main__":
    print "Crawling Wikipedia..."
    crawl('Carnegie_Mellon_University') # Seed page
    dl()
