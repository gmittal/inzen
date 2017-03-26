# Inzen
Information retrieval applications using Latent Semantic Analysis and Singular Value Matrix Decomposition. Gunn High School Analysis Honors Project 2017 by Daniel Zhu and Gautam Mittal

Requires Python 2.x+ and ```numpy```.

### Usage
``` $ python main.py "your search query"```

### Saved Results
Term-document and singular value decomposition matrices are saved after the initial execution of the program to avoid being regenerated every single time (saving compute resources and search time). This is useful if the desired reduced rank or the number of documents within the term-document matrix does not change. If you want to reset the program, simply run ``` $ rm -rf data/save/*``` to remove all of the saved files. The new term-document and SVD matrices will be automatically generated using your new documents or parameters the next time you run the program.