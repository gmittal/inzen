from __future__ import division
import re, glob, string, math, numpy as np

v_index = []

def init():
    global _docs
    _docs = glob.glob('data/*/*.txt') # Get all files from data directory
    prepare(_docs)


# Takes raw search query and an array of document paths
def prepare(docs):
    # Learn about all the terms
    for d in docs: 
        with open(d, 'r', encoding='utf8') as infh:
            doc = infh.read()
        tokenize(doc, True)

    # Create the term-document matrix
    term_matrix = [doc2vec(open(d, 'r', encoding='utf8').read()) for d in docs]
    term_matrix = np.asarray(term_matrix).transpose().astype(float)

    # tf-idf weighting
    for cv in range(0, len(docs)):
        col_vec = term_matrix[:,cv] # term-document vector

        for w in range(0, len(col_vec)):
            row_vec = term_matrix[w] # document-term vector
            tf = col_vec[w] / np.sum(col_vec)
            idf = math.log(len(docs) / (1 + np.count_nonzero(row_vec))) #wrong order of operations for idf 
            col_vec[w] = tf*idf # Assign the tf-idf weight instead of the raw term count

    # Singular value decomposition of term-document matrix
    U, D, V = np.linalg.svd(term_matrix, full_matrices=False)

    # Latent semantic analysis dimensionality reduction
    reduced_rank = 21 # Heuristic for determining reduced rank is not well-established
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
    
    
def query(query):    
    queryVec = doc2vec(query).astype(float)
    print(queryVec, _UT.shape, queryVec.shape)
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


# Tokenization and splitting into (non-lemmatized words)
def tokenize(t, new):
    doc = t.replace('\n', ' ').replace('\r', '')
    doc = re.sub(r'/[.,\/#!$%\^&\*;:{}=\-_`~()]/g', '', doc)
    doc = re.sub(r'/\s{2,}/g', '', doc)
    words = re.sub(r'/(\r\n|\n|\r)/gm', '', doc).lower()
    #words = words.translate(None, string.punctuation)
    words = words.split(' ');
    words = [k for k in words if len(k) != 0]

    if new:
        for w in words:
            if not (w in v_index):
                v_index.append(w)

    return words


# Turn a document into a term vector
def doc2vec(t):
    words = tokenize(t, False)
    v = [words.count(i) for i in v_index] # Get term counts for the document and put it in a vector
    return np.asarray(v)


if __name__ == '__main__':
    init() 
    print('querying openai')
    print(query('openai jobs'))
    print('querying james bond')
    print(query('james bond'))
    print('querying elon musk')
    print(query('elon musk'))