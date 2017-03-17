import re, string, numpy as np

v_index = []

def init():
    data = open('data/local/lab-rf-10,10.txt','r').read() # Open a plain text file
    print cosine_similarity(np.array([1, 2, 315]), np.array([2, 184, -1]))
    print doc2vec(data)

def cosine_similarity(np_v, np_u):
    return np.dot(np_v, np_u) / (np.linalg.norm(np_v) * np.linalg.norm(np_u))

def doc2vec(t):
    # Tokenization and splitting into (non-lemmatized words)
    doc = t.replace('\n', ' ').replace('\r', '')
    doc = re.sub(r'/[.,\/#!$%\^&\*;:{}=\-_`~()]/g', '', doc)
    doc = re.sub(r'/\s{2,}/g', '', doc)
    words = re.sub(r'/(\r\n|\n|\r)/gm', '', doc).lower().translate(None, string.punctuation).split(' ');
    words = [k for k in words if len(k) != 0]
    v = [] # Empty vector

    # Get term counts for the document and put it in a vector
    for w in words:
        if not (w in v_index):
            v_index.append(w)
    for i in v_index:
        v.append(words.count(i))

    return np.asarray(v)



if __name__ == '__main__':
    init()
