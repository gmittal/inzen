import re, glob, string, numpy as np

v_index = []

def init():
    docs = glob.glob('data/*/*.txt') # Get all files from data directory
    search('Query', docs)


# Takes raw search query and an array of document paths
def search(query, docs):
    # Learn about all the terms
    for d in docs:
        f = open(d, 'r').read()
        tokenize(f) # Not really a good idea to tokenize everything just to fill vector index, but ok for now

    # Create the term-document matrix
    term_matrix = [doc2vec(open(d, 'r').read()) for d in docs]
    term_matrix = np.asarray(term_matrix).transpose()

    # Singular value decomposition of term-document matrix
    U, D, V = np.linalg.svd(term_matrix)

    print term_matrix


# Find cosine of the angle between two vectors
def cosine_similarity(np_v, np_u):
    return np.dot(np_v, np_u) / (np.linalg.norm(np_v) * np.linalg.norm(np_u))

# Tokenization and splitting into (non-lemmatized words)
def tokenize(t):
    doc = t.replace('\n', ' ').replace('\r', '')
    doc = re.sub(r'/[.,\/#!$%\^&\*;:{}=\-_`~()]/g', '', doc)
    doc = re.sub(r'/\s{2,}/g', '', doc)
    words = re.sub(r'/(\r\n|\n|\r)/gm', '', doc).lower().translate(None, string.punctuation).split(' ');
    words = [k for k in words if len(k) != 0]
    for w in words:
        if not (w in v_index):
            v_index.append(w)

    return words

# Turn a document (words) into a term vector
def doc2vec(t):
    words = tokenize(t)
    v = [words.count(i) for i in v_index] # Get term counts for the document and put it in a vector
    return np.asarray(v)

if __name__ == '__main__':
    init()
