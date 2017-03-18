import urllib2, json

# List of topics you want to download from Wikipedia
q = [
    "Peter Norvig",
    "Latent semantic analysis",
    "Donald Trump",
    "Deep learning",
    "Barack Obama",
    "Larry Page",
    "Google",
    "Steve Jobs",
    "Miles Davis",
    "Wikipedia",
    "The Shawshank Redemption",
    "Macintosh",
    "Fibonacci",
    "2012 Tour de France",
    "Interstate 375 (Michigan)",
    "Star Trek",
    "BMW",
    "Jersey Shore shark attacks of 1916",
    "Maersk Alabama hijacking",
    "Captain Phillips (film)",
    "Boeing B-50 Superfortress",
    "Internet",
    "Google Hummingbird",
    "Nearest centroid classifier",
    "Wynton Marsalis",
    "Charlie Parker",
    "Dizzy Gillespie",
    "James Bond",
    "Peter Gunn",
    "Henry Mancini"
    ]

for n in q:
    r = urllib2.urlopen('https://en.wikipedia.org/w/api.php?format=json&action=query&prop=extracts&exintro=&explaintext=&titles='+urllib2.quote(n))
    d = json.load(r)
    for x in d["query"]["pages"]:
        s = d["query"]["pages"][x]["extract"].encode('utf-8')
        f = open("data/www/"+ n +".txt","w")
        f.write(s)
        f.close()
