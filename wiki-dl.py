import urllib2, json

# List of topics you want to download from Wikipedia
q = [
    "Seri_Rambai",
    "Licancabur",
    "Dorothy_Tarrant",
    "Emperor_Bing_of_Song",
    "Hermia and Lysander (painting)",
    "Dutch East India Company",
    "Jakarta",
    "Indonesia_Stock_Exchange",
    "Hong Kong Stock Exchange",
    "Psamtik I",
    "John Simmons (painter)",
    "The Beatles",
    "Mark Twain",
    "Adventures of Huckleberry Finn",
    "Adaptation",
    "Adaptation (film)",
    "Bolivia",
    "Constitution_of_Bolivia",
    "Racing 92",
    "Enigma machine",
    "Alan Turing",
    "Elizabeth II",
    "Hawaii",
    "J. J. Johnson",
    "Jazz trombone",
    "The Lord of the Rings",
    "Gandalf",
    "Jack Sparrow",
    "Pirates of the Caribbean",
    "Mahatma Gandhi",
    "Taekwondo",
    "Steven Lopez",
    "Usain Bolt",
    "Jeremy Wariner",
    "Michael Johnson (sprinter)",
    "Wayde van Niekerk",
    "World Heritage Site",
    "Machu Picchu",
    "Peru",
    "Avocado",
    "Avocado cake"
    ]

for n in q:
    r = urllib2.urlopen('https://en.wikipedia.org/w/api.php?format=json&action=query&prop=extracts&exintro=&explaintext=&titles='+urllib2.quote(n))
    d = json.load(r)
    for x in d["query"]["pages"]:
        s = d["query"]["pages"][x]["extract"].encode('utf-8')
        f = open("data/www/"+ n +".txt","w")
        f.write(s)
        f.close()
