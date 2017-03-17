import numpy as np

v_index = []

def init():
    data = open('data/local/lab-gm-10,10.txt','r').read() # Open a plain text file
    print cosine_similarity(np.array([1, 2, 315]), np.array([2, 184, -1]))

def cosine_similarity(np_v, np_u):
    return np.dot(np_v, np_u) / (np.linalg.norm(np_v) * np.linalg.norm(np_u))

def doc2vec(docText):
    

if __name__ == '__main__':
    init()
