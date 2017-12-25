from __future__ import division
import sys, os.path, re, glob, string, time, math, numpy as np
from tqdm import *

def init():
    global _docs

    if os.path.isfile('data/save/V.gz'):
        print "Loading..."
        _docs = [b for b in open('data/save/_docs.gz', 'r').read().split('\n')[:-1]]
        load()
    else:
        global v_index
        v_index = []
        _docs = glob.glob('data/*/*.txt')
        prepare(_docs[:10])

# Load previously saved matrices
def load():
    global _V, _invD, _UT, _N, v_index
    v_index = [b for b in open('data/save/v_index.gz', 'r').read().split('\n')[:-1]]
    _V = np.loadtxt('data/save/V.gz')
    D = np.loadtxt('data/save/D.gz')
    _UT = np.loadtxt('data/save/UT.gz')
    term_matrix = np.loadtxt('data/save/term_matrix.gz')
    _N = len(_docs)
    _invD = np.diag(1.0/D)

# Takes raw search query and an array of document paths
def prepare(docs):
    # Learn about all the terms
    for d in docs:
        with open(d, 'r') as infh:
            doc = infh.read()
        tokenize(doc, True)
        
    # Create the term-document matrix
    term_matrix = [doc2vec(open(d, 'r').read()) for d in docs]
    term_matrix = np.asarray(term_matrix).transpose().astype(float)

    # tf-idf weighting
    for cv in range(0, len(docs)):
        col_vec = term_matrix[:,cv] # term-document vector

        for w in range(0, len(col_vec)):
            row_vec = term_matrix[w] # document-term vector
            tf = col_vec[w] / (1 + np.sum(col_vec))
            idf = math.log(len(docs) / (1 + np.count_nonzero(row_vec))) #wrong order of operations for idf
            col_vec[w] = tf*idf # Assign the tf-idf weight instead of the raw term count

    # Singular value decomposition of term-document matrix
    U, D, V = np.linalg.svd(term_matrix, full_matrices=False)

    # Latent semantic analysis dimensionality reduction
    reduced_rank = 400 # Heuristic for determining reduced rank is not well-established
    U = U[:, :reduced_rank]
    #D = np.diag(D[:reduced_rank]) #[:reduced_rank, :reduced_rank]
    D = D[:reduced_rank]
    global _V, _invD, _UT, _N
    _V = V[:reduced_rank, :]
    # not used
    #low_term_matrix = np.dot(U, np.dot(D, V))
    _invD = np.diag(1.0/D)

    #np.linalg.inv(D)
    _UT = U.T
    _N = len(docs)

    np.savetxt('data/save/V.gz', _V)
    np.savetxt('data/save/D.gz', D)
    np.savetxt('data/save/UT.gz', _UT)
    np.savetxt('data/save/term_matrix.gz', term_matrix)
    f1 = open('data/save/v_index.gz', 'w')
    for item in v_index:
      f1.write("%s\n" % item)
    f1.close()
    f2 = open('data/save/_docs.gz', 'w')
    for item in _docs:
      f2.write("%s\n" % item)
    f2.close()

def search(query):
    queryVec = doc2vec(query).astype(float)
    # print(queryVec, _UT.shape, queryVec.shape)
    a = np.dot(_UT, queryVec)
    low_query = np.dot(_invD, a) # Reduce query vector dimensions as well

    # Get cosine similarities and search results
    # With latent semantic analysis
    index_r = {_docs[doc_vec]: cosine_similarity(low_query, _V[:,doc_vec]) for doc_vec in range(0, _N)}

    # Without latent semantic analysis
    # q_vec = doc2vec(query).astype(float)
    # index_r = {docs[doc_vec]: cosine_similarity(q_vec, term_matrix[:,doc_vec]) for doc_vec in range(0, len(docs))}
    results = sorted(index_r.items(), key=lambda x: x[1], reverse=True)
    return results



# Find cosine of the angle between two vectors
def cosine_similarity(np_v, np_u):
    return (np.dot(np_v, np_u) / (np.linalg.norm(np_v) * np.linalg.norm(np_u))) \
        if not (np.linalg.norm(np_v) * np.linalg.norm(np_u)) == 0 else 0

def word_split(text): return re.findall(r'\w+', text.lower())

# Tokenization and splitting into (non-lemmatized words)
def tokenize(t, new):
    doc = t.replace('\n', ' ').replace('\r', '')
    doc = re.sub(r'/[.,\/#!$%\^&\*;:{}=\-_`~()]/g', '', doc)
    doc = re.sub(r'/\s{2,}/g', '', doc)
    words = re.sub(r'/(\r\n|\n|\r)/gm', '', doc).lower()
    words = word_split(words)
    words = [k for k in words if len(k) != 0]

    if new:
        for w in words:
            if not (w in v_index):
                v_index.append(w)

    return words


# Turn a document into a term vector
def doc2vec(t):
    words = tokenize(t, False)
    vector = [words.count(i) for i in v_index] # Get term counts for the document and put it in a vector
    return np.asarray(vector)

# Pretty print array of search results
def pretty_print(r, myLen = None):
    if myLen is None:
        myLen = len(r)
    for t in range(myLen):
        print "#" + str(t+1) +": " + r[t][0] + " (" + str(r[t][1]) + ")"

if __name__ == '__main__':
    init() # This takes a while

    while True:
        query_input = raw_input('> ')

        if query_input == "/exit":
            break

        start = time.time()
        ranks = search(query_input)
        end = time.time()
        searchTime = round((end-start)*100)/100
        print "-"*25, "\nSearch Results for '"+ query_input +"' ("+ str(searchTime) + " seconds)"
        pretty_print(ranks, 10) # Print the top 10 search results
        print "\n"
