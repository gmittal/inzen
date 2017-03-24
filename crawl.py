from __future__ import unicode_literals
import requests, urllib2, json
from bs4 import BeautifulSoup

q = []

def crawl(u):
    parsed_html = BeautifulSoup(requests.get('https://en.wikipedia.org/wiki/'+u).text, "lxml")
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
        r = urllib2.urlopen('https://en.wikipedia.org/w/api.php?format=json&action=query&prop=extracts&exintro=&explaintext=&titles='+urllib2.quote(o))
        q.pop(0)
        d = json.load(r)
        try:
            for x in d["query"]["pages"]:
                s = d["query"]["pages"][x]["extract"].encode('utf-8')
                f = open("data/www/"+ o +".txt","w")
                f.write(s)
                f.close()
            crawl(o)
        except KeyError:
            crawl(q[0])


if __name__ == "__main__":
    print "Crawling Wikipedia..."
    crawl('Kind_of_Blue') # Seed page
    dl()
